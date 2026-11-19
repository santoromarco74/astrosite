<?php
// Copia questo file come config.php, compila i valori e caricalo A MANO via FTP
// nella cartella /commenti/ del sito. config.php NON va mai nel repository (è pubblico).

return [
    // Database MySQL creato dal pannello VHosting
    'db_host'     => 'localhost',
    'db_nome'     => 'NOME_DATABASE',
    'db_utente'   => 'UTENTE_DATABASE',
    'db_password' => 'PASSWORD_DATABASE',

    // Stringa casuale di almeno 32 caratteri (firma i moduli e le impronte degli IP).
    // Generala con:  php -r "echo bin2hex(random_bytes(32)), PHP_EOL;"
    'segreto' => 'INCOLLA_QUI_LA_STRINGA_CASUALE',

    // Hash della password della pagina di moderazione (NON la password in chiaro).
    // Generalo con:  php -r "echo password_hash('LA_TUA_PASSWORD', PASSWORD_DEFAULT), PHP_EOL;"
    'password_moderazione' => 'INCOLLA_QUI_L_HASH',

    // Dove arriva l'avviso di ogni nuovo commento da approvare
    'email_avvisi'   => 'tuo@indirizzo.it',
    // Mittente degli avvisi: meglio un indirizzo del dominio, così non finiscono in spam
    'email_mittente' => 'noreply@lamusicadelsanto.it',

    'url_sito' => 'https://lamusicadelsanto.it',
];
