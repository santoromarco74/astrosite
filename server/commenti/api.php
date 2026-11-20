<?php
// API pubblica dei commenti.
//   GET  api.php?articolo=<slug>  -> commenti approvati dell'articolo + gettone per il modulo
//   POST api.php (JSON)           -> nuovo commento, che resta in attesa di approvazione

declare(strict_types=1);
define('LMS_COMMENTI', true);
require_once __DIR__ . '/lib.php';

header('X-Robots-Tag: noindex');

$metodo = $_SERVER['REQUEST_METHOD'] ?? 'GET';

try {
    if ($metodo === 'GET') elenco();
    elseif ($metodo === 'POST') nuovo();
    else rispondi(['errore' => 'Metodo non ammesso.'], 405);
} catch (PDOException $e) {
    error_log('commenti: ' . $e->getMessage());
    rispondi(['errore' => 'I commenti non sono disponibili in questo momento.'], 503);
}

function elenco(): void {
    $slug = (string) ($_GET['articolo'] ?? '');
    if (!slug_valido($slug)) rispondi(['errore' => 'Articolo non valido.'], 400);

    $st = db()->prepare('SELECT id, parent_id, nome, testo, creato FROM ' . TABELLA .
        " WHERE articolo = ? AND stato = 'approvato' ORDER BY creato ASC, id ASC");
    $st->execute([$slug]);
    $commenti = array_map(function ($r) {
        return [
            'id' => (int) $r['id'],
            'risposta_a' => $r['parent_id'] !== null ? (int) $r['parent_id'] : null,
            'nome' => $r['nome'],
            'testo' => $r['testo'],
            'data' => date('c', strtotime($r['creato'])),
        ];
    }, $st->fetchAll());

    $ora = (string) time();
    rispondi(['commenti' => $commenti, 'gettone' => $ora . '.' . firma('modulo|' . $slug . '|' . $ora)]);
}

function nuovo(): void {
    $d = json_decode((string) file_get_contents('php://input', false, null, 0, 20000), true);
    if (!is_array($d)) rispondi(['errore' => 'Richiesta non valida.'], 400);

    // trappola per i bot: campo nascosto che un umano non vede e non compila
    if (trim((string) ($d['sito'] ?? '')) !== '') rispondi(['ok' => true]);

    $slug = (string) ($d['articolo'] ?? '');
    if (!articolo_esiste($slug)) rispondi(['errore' => 'Articolo non trovato.'], 400);

    // gettone firmato: il modulo deve essere stato caricato da questa pagina, né troppo presto né troppo tardi
    $parti = explode('.', (string) ($d['gettone'] ?? ''), 2);
    if (count($parti) !== 2 || !hash_equals(firma('modulo|' . $slug . '|' . $parti[0]), $parti[1])) {
        rispondi(['errore' => 'Il modulo è scaduto: ricarica la pagina e riprova.'], 400);
    }
    $eta = time() - (int) $parti[0];
    if ($eta < TEMPO_MINIMO) rispondi(['errore' => 'Troppo veloce: riprova tra qualche secondo.'], 429);
    if ($eta > TEMPO_MASSIMO) rispondi(['errore' => 'Il modulo è scaduto: ricarica la pagina e riprova.'], 400);

    if (($d['privacy'] ?? false) !== true) rispondi(['errore' => "Serve il consenso al trattamento dei dati."], 400);

    $nome = pulisci((string) ($d['nome'] ?? ''));
    $email = trim((string) ($d['email'] ?? ''));
    $testo = pulisci((string) ($d['testo'] ?? ''), true);

    if ($nome === '' || lunghezza($nome) > MAX_NOME) rispondi(['errore' => 'Scrivi un nome (massimo ' . MAX_NOME . ' caratteri).'], 400);
    if (strlen($email) > MAX_EMAIL || !filter_var($email, FILTER_VALIDATE_EMAIL)) rispondi(['errore' => "L'indirizzo email non sembra valido."], 400);
    if (lunghezza($testo) < 2 || lunghezza($testo) > MAX_TESTO) rispondi(['errore' => 'Il commento deve stare tra 2 e ' . MAX_TESTO . ' caratteri.'], 400);
    if (preg_match_all('~https?://~i', $testo) > 2) rispondi(['errore' => 'Troppi link nel commento (massimo 2).'], 400);

    $parent = null;
    if (isset($d['risposta_a']) && $d['risposta_a'] !== null && $d['risposta_a'] !== '') {
        $parent = (int) $d['risposta_a'];
        $st = db()->prepare('SELECT id FROM ' . TABELLA . " WHERE id = ? AND articolo = ? AND stato = 'approvato'");
        $st->execute([$parent, $slug]);
        if (!$st->fetch()) rispondi(['errore' => 'Il commento a cui rispondi non esiste più.'], 400);
        if (profondita($parent) >= MAX_PROFONDITA) rispondi(['errore' => 'Questa discussione è già annidata al massimo: rispondi al commento sopra.'], 400);
    }

    $ip = impronta_ip();
    $st = db()->prepare('SELECT COUNT(*) AS n FROM ' . TABELLA . ' WHERE ip_hash = ? AND creato > ?');
    $st->execute([$ip, date('Y-m-d H:i:s', time() - FINESTRA_INVII)]);
    if ((int) $st->fetch()['n'] >= LIMITE_INVII) rispondi(['errore' => 'Hai inviato molti commenti di fila: riprova tra qualche minuto.'], 429);

    $ins = db()->prepare('INSERT INTO ' . TABELLA . " (articolo, parent_id, nome, email, testo, stato, ip_hash, creato) VALUES (?, ?, ?, ?, ?, 'attesa', ?, ?)");
    $ins->execute([$slug, $parent, $nome, $email, $testo, $ip, date('Y-m-d H:i:s')]);

    avvisa_marco($slug, $nome, $email, $testo);
    rispondi(['ok' => true, 'messaggio' => 'Grazie! Il commento comparirà dopo l\'approvazione.']);
}

function avvisa_marco(string $slug, string $nome, string $email, string $testo): void {
    $corpo = "Nuovo commento in attesa su " . url_sito() . "/$slug/\n\n"
        . "Nome: $nome\nEmail: $email\n\n$testo\n\n"
        . "Approva o elimina: " . url_sito() . "/commenti/moderazione.php\n";
    // se l'email non parte il commento resta comunque salvato: l'errore va solo nel log
    invia_email(config()['email_avvisi'], 'Nuovo commento da approvare: ' . $slug, $corpo);
}
