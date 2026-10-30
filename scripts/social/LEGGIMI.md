# Grafiche social (tema «Biglietti»)

Stessi colori e caratteri del sito: fondo carta chiara, inchiostro scuro, biglietto terracotta;
Big Shoulders Display (titoli), Literata (testi), Courier Prime (fascia, date, dettagli).
Struttura: fascia «Accadde il …», nome del sito, biglietto con foto, perforazione, sezione, titolo,
occhiello e data d'epoca, credito della foto, due brevi testi, barra «All'interno».

1. Copia `dati/bill-wyman-90-anni.json` in `dati/<slug>.json` e cambia i testi
   (titolo con `<br>` per andare a capo; `fuoco` = punto della foto da tenere al centro, es. "50% 30%").
   La fascia in alto è «Accadde il <data_evento>»; per l'attualità aggiungi il campo `fascia`
   (es. "In uscita il 30 ottobre 2026", "Dal vivo il 12 novembre 2026").
   Il campo `sezione` è la sezione stampata sul biglietto (di default «Storie», es. "Album").
2. `NODE_PATH=$(npm root -g) node scripts/social/genera.cjs scripts/social/dati/<slug>.json`
   (serve Playwright; se manca: `npm i -g playwright`).
3. Escono `public/social/<slug>-ig.jpg` (1080×1350, JPEG per Instagram), `public/social/<slug>-fb.png` (1200×630)
   e `public/social/<slug>-storia.jpg` (1080×1920, storia Instagram: lo spazio vuoto sotto la freccia è il posto dello sticker «Link»,
   che Marco aggiunge dall'app; serve il campo `occhiello_storia`).
   Se compare «il contenuto esce dalla tela», accorcia titolo, occhiello o testi.
