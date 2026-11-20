<?php
// Funzioni comuni del sistema di commenti. Non si apre dal browser (bloccato da .htaccess).
// Compatibile con PHP 7.4 e successivi.

declare(strict_types=1);

if (!defined('LMS_COMMENTI')) { http_response_code(403); exit; }

const TABELLA = 'lms_commenti';   // se cambia, va cambiato anche nel CREATE TABLE di db()
const MAX_NOME = 60;
const MAX_EMAIL = 190;
const MAX_TESTO = 3000;
const MAX_PROFONDITA = 3;         // commento -> risposta -> risposta alla risposta
const TEMPO_MINIMO = 4;           // secondi: un umano non compila il modulo più in fretta
const TEMPO_MASSIMO = 6 * 3600;   // il modulo scade dopo 6 ore
const LIMITE_INVII = 3;           // al massimo 3 commenti...
const FINESTRA_INVII = 600;       // ...ogni 10 minuti dallo stesso indirizzo

// Nomi delle voci obbligatorie di config.php (solo i nomi: i valori stanno sul server)
const CHIAVI_CONFIG = [
    'db_host',
    'db_nome',
    'db_utente',
    'db_password',
    'segreto',
    'password_moderazione',
    'email_avvisi',
];

function config(): array {
    static $c = null;
    if ($c !== null) return $c;
    $file = __DIR__ . '/config.php';
    if (!is_file($file)) {
        rispondi(['errore' => 'Commenti non ancora configurati.'], 503);
    }
    $c = require_once $file;
    foreach (CHIAVI_CONFIG as $k) {
        if (!isset($c[$k]) || $c[$k] === '') rispondi(['errore' => "Configurazione incompleta: manca $k."], 503);
    }
    if (strlen($c['segreto']) < 32) rispondi(['errore' => 'Configurazione: il segreto deve avere almeno 32 caratteri.'], 503);
    return $c;
}

function db(): PDO {
    static $pdo = null;
    if ($pdo !== null) return $pdo;
    $c = config();
    $pdo = new PDO(
        'mysql:host=' . $c['db_host'] . ';dbname=' . $c['db_nome'] . ';charset=utf8mb4',
        $c['db_utente'], $c['db_password'],
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, PDO::ATTR_EMULATE_PREPARES => false]
    );
    // la tabella si crea da sola al primo utilizzo
    $pdo->exec("CREATE TABLE IF NOT EXISTS lms_commenti (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        articolo VARCHAR(200) NOT NULL,
        parent_id INT UNSIGNED NULL,
        nome VARCHAR(60) NOT NULL,
        email VARCHAR(190) NOT NULL,
        testo TEXT NOT NULL,
        stato VARCHAR(12) NOT NULL DEFAULT 'attesa',
        ip_hash CHAR(64) NOT NULL DEFAULT '',
        creato DATETIME NOT NULL,
        approvato DATETIME NULL,
        KEY idx_articolo (articolo, stato),
        KEY idx_ip (ip_hash, creato)
    ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
    return $pdo;
}

function rispondi(array $dati, int $codice = 200): void {
    http_response_code($codice);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($dati, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function firma(string $dato): string {
    return hash_hmac('sha256', $dato, config()['segreto']);
}

// L'indirizzo IP non viene salvato: solo un'impronta, usata per il limite di invii
// e cancellata quando il commento viene approvato.
function impronta_ip(): string {
    return firma('ip|' . ($_SERVER['REMOTE_ADDR'] ?? ''));
}

function slug_valido(string $s): bool {
    return (bool) preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $s) && strlen($s) <= 200;
}

// Esiste davvero l'articolo? Il sito statico sta nella cartella sopra a questa.
function articolo_esiste(string $slug): bool {
    return slug_valido($slug) && is_file(dirname(__DIR__) . '/' . $slug . '/index.html');
}

function lunghezza(string $s): int {
    return function_exists('mb_strlen') ? mb_strlen($s, 'UTF-8') : strlen($s);
}

// Toglie caratteri di controllo (tranne a capo) e spazi in eccesso.
function pulisci(string $s, bool $multiriga = false): string {
    $s = str_replace(["\r\n", "\r"], "\n", $s);
    $s = preg_replace($multiriga ? '/[^\P{C}\n]/u' : '/\p{C}/u', '', $s) ?? '';
    if ($multiriga) $s = preg_replace("/\n{3,}/", "\n\n", $s) ?? '';
    else $s = preg_replace('/\s+/u', ' ', $s) ?? '';
    return trim($s);
}

function profondita(int $id): int {
    $p = 0;
    $st = db()->prepare('SELECT parent_id FROM ' . TABELLA . ' WHERE id = ?');
    while ($id && $p <= MAX_PROFONDITA + 1) {
        $st->execute([$id]);
        $r = $st->fetch();
        if (!$r) break;
        $p++;
        $id = (int) ($r['parent_id'] ?? 0);
    }
    return $p;
}

// Cancella un commento e tutte le risposte che dipendono da lui.
function elimina_con_risposte(int $id): int {
    $da_fare = [$id];
    $tutti = [];
    $st = db()->prepare('SELECT id FROM ' . TABELLA . ' WHERE parent_id = ?');
    while ($da_fare) {
        $x = array_pop($da_fare);
        $tutti[] = $x;
        $st->execute([$x]);
        foreach ($st->fetchAll() as $r) $da_fare[] = (int) $r['id'];
    }
    $segnaposto = implode(',', array_fill(0, count($tutti), '?'));
    $del = db()->prepare('DELETE FROM ' . TABELLA . " WHERE id IN ($segnaposto)");
    $del->execute($tutti);
    return $del->rowCount();
}

function url_sito(): string {
    $c = config();
    return rtrim($c['url_sito'] ?? 'https://lamusicadelsanto.it', '/');
}

// ---------------------------------------------------------------------------
// Email. Se in config.php c'è smtp_host, l'avviso parte via SMTP autenticato con una casella
// vera del dominio (il metodo più affidabile). Altrimenti usa mail() del PHP.
// Ritorna '' se l'invio è andato, altrimenti il motivo dell'errore (che finisce anche nel log PHP).

function invia_email(string $a, string $oggetto, string $testo): string {
    $c = config();
    $mittente = $c['email_mittente'] ?? 'noreply@lamusicadelsanto.it';
    $dominio = substr((string) strrchr($mittente, '@'), 1) ?: 'lamusicadelsanto.it';
    $intestazioni = [
        'Date: ' . date('r'),
        'From: La musica del Santo <' . $mittente . '>',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $dominio . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    $oggetto = '=?UTF-8?B?' . base64_encode($oggetto) . '?=';
    $corpo = rtrim(chunk_split(base64_encode($testo), 76, "\r\n"));

    if (!empty($c['smtp_host'])) {
        try {
            smtp_invia($c, $mittente, $a, implode("\r\n", array_merge($intestazioni, ['To: <' . $a . '>', 'Subject: ' . $oggetto])) . "\r\n\r\n" . $corpo);
            return '';
        } catch (Throwable $e) {
            $errore = 'SMTP: ' . $e->getMessage();
            error_log('commenti: ' . $errore);
            return $errore;
        }
    }

    if (!function_exists('mail')) {
        error_log('commenti: la funzione mail() è disattivata su questo hosting');
        return 'la funzione mail() è disattivata su questo hosting: configura smtp_host';
    }
    // -f imposta il mittente "di busta": molti hosting condivisi scartano le email senza
    $ok = mail($a, $oggetto, $corpo, implode("\r\n", $intestazioni), '-f' . $mittente);
    if (!$ok) {
        error_log('commenti: mail() ha rifiutato l\'invio a ' . $a);
        return 'il server ha rifiutato l\'invio con mail(): configura smtp_host';
    }
    return '';
}

function smtp_invia(array $c, string $da, string $a, string $messaggio): void {
    $sicurezza = strtolower((string) ($c['smtp_sicurezza'] ?? 'ssl'));   // ssl (porta 465) | tls (587) | nessuna
    $porta = (int) ($c['smtp_porta'] ?? ($sicurezza === 'ssl' ? 465 : 587));
    $host = ($sicurezza === 'ssl' ? 'ssl://' : 'tcp://') . $c['smtp_host'] . ':' . $porta;
    $s = @stream_socket_client($host, $errno, $errstr, 15);
    if (!$s) {
        throw new RuntimeException("connessione a {$c['smtp_host']}:$porta non riuscita ($errstr)");
    }
    stream_set_timeout($s, 15);
    $leggi = function (int $atteso) use ($s): string {
        $risposta = '';
        while (($riga = fgets($s, 1024)) !== false) {
            $risposta .= $riga;
            if (strlen($riga) < 4 || $riga[3] !== '-') {
                break;
            }
        }
        if ($risposta === '') {
            throw new RuntimeException('nessuna risposta dal server di posta (tempo scaduto)');
        }
        if ((int) substr($risposta, 0, 3) !== $atteso) {
            throw new RuntimeException('risposta inattesa del server: ' . trim($risposta));
        }
        return $risposta;
    };
    $scrivi = function (string $comando, int $atteso) use ($s, $leggi): string {
        fwrite($s, $comando . "\r\n");
        return $leggi($atteso);
    };
    try {
        $leggi(220);
        $nome = gethostname() ?: 'lamusicadelsanto.it';
        $scrivi('EHLO ' . $nome, 250);
        if ($sicurezza === 'tls') {
            $scrivi('STARTTLS', 220);
            // solo TLS 1.2 o 1.3: le versioni più vecchie non sono più sicure
            $metodo = STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | (defined('STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT') ? STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT : 0);
            if (!stream_socket_enable_crypto($s, true, $metodo)) {
                throw new RuntimeException('STARTTLS non riuscito');
            }
            $scrivi('EHLO ' . $nome, 250);
        }
        if (!empty($c['smtp_utente'])) {
            $scrivi('AUTH LOGIN', 334);
            $scrivi(base64_encode((string) $c['smtp_utente']), 334);
            $scrivi(base64_encode((string) ($c['smtp_password'] ?? '')), 235);
        }
        $scrivi('MAIL FROM:<' . $da . '>', 250);
        $scrivi('RCPT TO:<' . $a . '>', 250);
        $scrivi('DATA', 354);
        // le righe che iniziano con un punto vanno raddoppiate (regola del protocollo SMTP)
        $scrivi(preg_replace('/^\./m', '..', $messaggio) . "\r\n.", 250);
        $scrivi('QUIT', 221);
    } finally {
        fclose($s);
    }
}
