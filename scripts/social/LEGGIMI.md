# Grafiche social (tema «Sintonia»)

Stessi colori e caratteri del sito: fondo salvia, antracite, ambra; Zilla Slab, Source Serif 4, DM Mono.
Struttura: fascia «Accadde il …», testata, scala FM con lancetta, data d'epoca e «Prezzo: un ascolto»,
titolo, occhiello, foto come copertina di LP con il disco che esce, due brevi testi, barra «All'interno».

1. Copia `dati/bill-wyman-90-anni.json` in `dati/<slug>.json` e cambia i testi
   (titolo con `<br>` per andare a capo; `fuoco` = punto della foto da tenere al centro, es. "50% 30%").
2. `NODE_PATH=$(npm root -g) node scripts/social/genera.cjs scripts/social/dati/<slug>.json`
   (serve Playwright; se manca: `npm i -g playwright`).
3. Escono `public/social/<slug>-ig.jpg` (1080×1350, JPEG per Instagram), `public/social/<slug>-fb.png` (1200×630)
   e `public/social/<slug>-storia.jpg` (1080×1920, storia Instagram: lo spazio vuoto sotto la freccia è il posto dello sticker «Link»,
   che Marco aggiunge dall'app; serve il campo `occhiello_storia`).
   Se compare «il contenuto esce dalla tela», accorcia titolo, occhiello o testi.
