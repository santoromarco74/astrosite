# Commenti — lamusicadelsanto.it

Sistema di commenti fatto in casa: PHP + MySQL sull'hosting VHosting, nessun servizio esterno.

- `api.php` — legge i commenti approvati e riceve quelli nuovi (che restano **in attesa**)
- `moderazione.php` — pagina protetta da password per approvare o eliminare
- `lib.php` — funzioni comuni (non si apre dal browser)
- `.htaccess` — nella cartella si possono aprire solo `api.php` e `moderazione.php`
- `config.example.php` — modello della configurazione

L'interfaccia sul sito è `src/components/Commenti.astro`, in fondo a ogni articolo.

## Regole scelte

- Moderazione **prima** della pubblicazione: niente compare senza approvazione.
- Nome ed email **obbligatori**; l'email non viene mai mostrata.
- Risposte annidate fino a 3 livelli.
- Antispam: campo trappola nascosto, modulo firmato con tempo minimo (4 s) e scadenza (6 h),
  massimo 3 commenti ogni 10 minuti dallo stesso indirizzo, massimo 2 link per commento.
- Privacy: l'IP non viene salvato, solo un'impronta cifrata che si cancella all'approvazione.
  Nessun cookie per i lettori. Serve il consenso esplicito (casella nel modulo).
- Eliminando un commento si eliminano anche le sue risposte.

## Messa in funzione (una volta sola)

1. **Database.** Dal pannello VHosting crea un database MySQL e un utente con tutti i permessi
   su quel database. La tabella `lms_commenti` si crea da sola al primo utilizzo.
2. **Configurazione.** Copia `config.example.php` come `config.php` e compila i valori
   (le istruzioni per generare segreto e hash della password sono nel file).
3. **Carica `config.php` a mano** via FTP nella cartella `/commenti/` del sito.
   Non metterlo mai nel repository: è pubblico (`.gitignore` lo esclude, e la pubblicazione
   si blocca se lo trova).
4. Al prossimo merge su `main` la pubblicazione carica il resto in `/commenti/`.
5. **Prova:** apri un articolo, lascia un commento, controlla che arrivi l'email, entra in
   `https://lamusicadelsanto.it/commenti/moderazione.php` e approvalo.

## Se qualcosa non va

- *«I commenti non sono disponibili»*: manca `config.php`, oppure i dati del database sono sbagliati
  (l'errore preciso finisce nel log degli errori PHP del pannello VHosting).
- *`api.php` risponde 403*: il server non ha riaperto il PHP nella cartella; controlla che
  `/commenti/.htaccess` sia stato caricato.
- *Non arrivano le email*: verifica che `email_mittente` sia una casella del dominio
  lamusicadelsanto.it; i commenti si vedono comunque nella pagina di moderazione.
- In sviluppo (`npm run dev`) non c'è PHP: la sezione mostra solo il messaggio di non disponibilità.

## Privacy policy

La privacy policy del sito (iubenda) va aggiornata con la nuova raccolta di dati: nome, email
e testo dei commenti, finalità «pubblicazione e gestione dei commenti», conservazione finché
il commento resta online.
