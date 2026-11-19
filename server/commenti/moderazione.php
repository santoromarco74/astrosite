<?php
// Pagina di moderazione dei commenti: lamusicadelsanto.it/commenti/moderazione.php
// Protetta da password (quella il cui hash sta in config.php).

declare(strict_types=1);
define('LMS_COMMENTI', true);
require __DIR__ . '/lib.php';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'");

session_name('lms_moderazione');
session_set_cookie_params(['lifetime' => 0, 'path' => '/commenti/', 'secure' => true, 'httponly' => true, 'samesite' => 'Strict']);
session_start();

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

function csrf(): string {
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function controlla_csrf(): void {
    if (!hash_equals(csrf(), (string) ($_POST['csrf'] ?? ''))) { http_response_code(400); exit('Richiesta non valida: ricarica la pagina.'); }
}

$messaggio = '';
$post = ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';

if ($post && ($_POST['azione'] ?? '') === 'entra') {
    controlla_csrf();
    if (password_verify((string) ($_POST['password'] ?? ''), config()['password_moderazione'])) {
        session_regenerate_id(true);
        $_SESSION['dentro'] = true;
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
        header('Location: moderazione.php', true, 303);
        exit;
    }
    sleep(2); // rallenta chi prova password a caso
    $messaggio = 'Password sbagliata.';
}

$dentro = !empty($_SESSION['dentro']);

if ($dentro && $post) {
    controlla_csrf();
    $azione = (string) ($_POST['azione'] ?? '');
    $id = (int) ($_POST['id'] ?? 0);
    if ($azione === 'esci') {
        $_SESSION = [];
        session_destroy();
        header('Location: moderazione.php', true, 303);
        exit;
    }
    if ($azione === 'approva' && $id) {
        $st = db()->prepare('UPDATE ' . TABELLA . " SET stato = 'approvato', approvato = ?, ip_hash = '' WHERE id = ? AND stato = 'attesa'");
        $st->execute([date('Y-m-d H:i:s'), $id]);
        $messaggio = $st->rowCount() ? 'Commento approvato e pubblicato.' : 'Commento già approvato o non trovato.';
    }
    if ($azione === 'elimina' && $id) {
        $n = elimina_con_risposte($id);
        $messaggio = $n > 1 ? "Eliminati $n commenti (il commento e le sue risposte)." : ($n ? 'Commento eliminato.' : 'Commento non trovato.');
    }
}

?><!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Moderazione commenti — La musica del Santo</title>
<style>
  body { margin: 0; background: #F5F2EC; color: #1C1A1F; font: 17px/1.5 'Courier New', monospace; }
  main { max-width: 860px; margin: 0 auto; padding: 24px 16px 60px; }
  h1 { font: 900 34px/1 Impact, 'Arial Narrow', sans-serif; text-transform: uppercase; margin: 0 0 6px; }
  h2 { font: 800 24px/1.1 Impact, 'Arial Narrow', sans-serif; text-transform: uppercase; margin: 36px 0 12px; border-top: 3px dashed #1C1A1F; padding-top: 12px; }
  .msg { background: #7FA996; padding: 10px 14px; border-radius: 6px; }
  .c { background: #fff; border: 1.5px dashed #1C1A1F; border-radius: 8px; padding: 14px 16px; margin: 0 0 14px; }
  .meta { font-size: 14px; color: #5A5463; margin: 0 0 8px; }
  .testo { font-family: Georgia, serif; white-space: pre-wrap; overflow-wrap: anywhere; margin: 0 0 10px; }
  .rif { font-size: 14px; border-left: 3px solid #9A93A3; padding-left: 10px; color: #5A5463; margin: 0 0 10px; }
  form.inline { display: inline; }
  button { font: 700 15px 'Courier New', monospace; padding: 8px 14px; border: 2px solid #1C1A1F; border-radius: 4px; background: #F5F2EC; cursor: pointer; margin-right: 6px; }
  button.si { background: #1C1A1F; color: #F5F2EC; }
  button.no { border-color: #A33A1C; color: #A33A1C; }
  input[type=password] { font: inherit; padding: 8px; border: 2px solid #1C1A1F; border-radius: 4px; }
  a { color: #A33A1C; }
  .esci { float: right; }
</style>
</head>
<body><main>
<?php if (!$dentro): ?>
  <h1>Moderazione commenti</h1>
  <?php if ($messaggio): ?><p class="msg"><?= h($messaggio) ?></p><?php endif; ?>
  <form method="post">
    <input type="hidden" name="csrf" value="<?= h(csrf()) ?>">
    <input type="hidden" name="azione" value="entra">
    <p><label>Password <input type="password" name="password" autocomplete="current-password" required autofocus></label>
    <button class="si">Entra</button></p>
  </form>
<?php else:
    $attesa = db()->query('SELECT c.*, p.nome AS p_nome, p.testo AS p_testo FROM ' . TABELLA . ' c LEFT JOIN ' . TABELLA .
        " p ON p.id = c.parent_id WHERE c.stato = 'attesa' ORDER BY c.creato ASC")->fetchAll();
    $recenti = db()->query('SELECT * FROM ' . TABELLA . " WHERE stato = 'approvato' ORDER BY approvato DESC LIMIT 30")->fetchAll();
?>
  <form method="post" class="inline esci"><input type="hidden" name="csrf" value="<?= h(csrf()) ?>"><button name="azione" value="esci">Esci</button></form>
  <h1>Moderazione commenti</h1>
  <?php if ($messaggio): ?><p class="msg"><?= h($messaggio) ?></p><?php endif; ?>

  <h2>In attesa (<?= count($attesa) ?>)</h2>
  <?php if (!$attesa): ?><p>Nessun commento da approvare.</p><?php endif; ?>
  <?php foreach ($attesa as $c): ?>
    <div class="c">
      <p class="meta"><strong><?= h($c['nome']) ?></strong> · <?= h($c['email']) ?> · <?= h(date('d/m/Y H:i', strtotime($c['creato']))) ?><br>
        su <a href="<?= h(url_sito() . '/' . $c['articolo'] . '/') ?>" target="_blank" rel="noopener"><?= h($c['articolo']) ?></a></p>
      <?php if ($c['parent_id']): ?><p class="rif">In risposta a <strong><?= h((string) $c['p_nome']) ?></strong>: <?= h(mb_strimwidth((string) $c['p_testo'], 0, 160, '…', 'UTF-8')) ?></p><?php endif; ?>
      <p class="testo"><?= h($c['testo']) ?></p>
      <form method="post" class="inline"><input type="hidden" name="csrf" value="<?= h(csrf()) ?>"><input type="hidden" name="id" value="<?= (int) $c['id'] ?>">
        <button class="si" name="azione" value="approva">Approva</button>
        <button class="no" name="azione" value="elimina">Elimina</button>
      </form>
    </div>
  <?php endforeach; ?>

  <h2>Pubblicati di recente</h2>
  <?php if (!$recenti): ?><p>Ancora nessun commento pubblicato.</p><?php endif; ?>
  <?php foreach ($recenti as $c): ?>
    <div class="c">
      <p class="meta"><strong><?= h($c['nome']) ?></strong> · <?= h($c['email']) ?> · <?= h(date('d/m/Y H:i', strtotime($c['creato']))) ?>
        · su <a href="<?= h(url_sito() . '/' . $c['articolo'] . '/#commento-' . $c['id']) ?>" target="_blank" rel="noopener"><?= h($c['articolo']) ?></a></p>
      <p class="testo"><?= h($c['testo']) ?></p>
      <form method="post" class="inline"><input type="hidden" name="csrf" value="<?= h(csrf()) ?>"><input type="hidden" name="id" value="<?= (int) $c['id'] ?>">
        <button class="no" name="azione" value="elimina">Elimina (con le risposte)</button>
      </form>
    </div>
  <?php endforeach; ?>
<?php endif; ?>
</main></body>
</html>
