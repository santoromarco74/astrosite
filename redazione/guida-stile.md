# Guida di stile — La musica del Santo

Ricavata dagli articoli pubblicati tra settembre e novembre 2026 (Back to Black, Chuck Berry,
Bill Wyman, Leonard Cohen, Led Zeppelin IV, Sting, Atom Heart Mother, l'Olandese Volante).
Vale per tutti gli agenti della redazione. Se un articolo nuovo di Marco si discosta da qui,
ha ragione l'articolo: aggiornate la guida.

## Identità

- Sottotitolo del sito: «Guida semiseria per autostoppisti musicali».
- Metafora di casa: il concerto e il biglietto (biglietteria, «in cartellone», «ingresso»).
- Pubblico: appassionati italiani, non addetti ai lavori. Si racconta, non si recensisce.
- Tono: semiserio, caldo, curioso. Mai accademico, mai agiografico («niente santini»).
  Le ombre degli artisti si dicono, «senza giri di parole», ma senza morbosità.

## Sezioni (campo `categories`)

| Slug | Nome | Quando |
|---|---|---|
| `album` | Album | Anniversario di un disco (25, 30, 35, 40, 50, 55… anni) |
| `storie` | Storie | Compleanni tondi, anniversari di morte, vite e carriere |
| `attualita` | Attualità | Morti recenti, uscite, tour, notizie |
| `film` | Film & Musical | Film musicali, biopic, musical |
| `imperdibili` | Imperdibili | Dischi da ascoltare almeno una volta, senza anniversario |

## Ritmo editoriale

- Un pezzo ogni 4-5 giorni circa, quasi sempre agganciato a un anniversario tondo
  pubblicato **il giorno stesso** dell'anniversario.
- Lunghezza: 950-1.600 parole (lettura 4-6 minuti).

## Struttura tipica

1. **Attacco**: la data e il numero in grassetto nella prima o seconda frase
   («Il **24 ottobre 2026** **Bill Wyman** compie **90 anni**»). Spesso un aggancio al pezzo
   precedente («Dopo i cento anni di Chuck Berry…»).
2. `## Il racconto di …` — le origini, con 1-3 `###` di episodi.
3. `## L'approfondimento: …` — il cuore: come è nato il disco, la svolta, i retroscena.
4. Facoltativo: `## L'eredità …` / una sezione sulle ombre.
5. `## Se dovessi dire cosa rappresenta…` — la sola parte in prima persona singolare, il giudizio.
6. Galleria: 2-3 immagini una per riga, con didascalia e credito.
7. `## Se volete approfondire` — cosa ascoltare/guardare, in che ordine, link a pezzi interni.
8. **Chiusa**: una domanda ai lettori («E voi, qual è la vostra canzone di…?»).

I titoli dei paragrafi sono frasi con un'immagine concreta, non etichette
(«Il concerto in pigiama», «Una casa fredda, un camion e mille sterline a settimana»).

## Voce

- Ci si rivolge ai lettori con il **voi**; il blog parla con il **noi** («il nostro pezzo su…»).
- Formule ricorrenti, da usare con misura (una o due per pezzo, non tutte):
  «La cosa più pazzesca è che…», «Per carità, …», «Diciamo che…», «Quello che in pochi sanno è che…»,
  «Se ve lo state chiedendo: sì, …», «E sapete cosa…?», «se ve lo raccontassero al bar, non ci credereste».
- Le **chicche per il pubblico italiano** sono un marchio di fabbrica (De André e «Suzanne»,
  Wyman e Dario Argento): cercatele sempre.
- Dubbi dichiarati onestamente: «Dettaglio da prendere con le molle, perché lo racconta soprattutto
  una sola fonte», «la cifra varia a seconda delle fonti», «è la sua versione dei fatti».
- Citazioni brevi tra «caporali», corsivo per i titoli di libri, film e programmi.

## Formattazione

- **Grassetto** su date, numeri, età, nomi alla prima occorrenza.
- Album e film in corsivo (*Songs of Leonard Cohen*, a volte grassetto+corsivo alla prima occorrenza);
  canzoni tra caporali («Hallelujah»).
- Virgolette e apostrofi tipografici: « », ’.
- Link esterni: Wikipedia (it o en) sulla prima occorrenza di artista, disco, brano;
  fonti autorevoli per i fatti discussi.
- **Link interni** ad altri articoli del blog ogni volta che c'è un nesso: `[testo](/slug/)`.
- Player: un link Spotify o YouTube da solo su una riga diventa un player incorporato.

## Frontmatter

```yaml
title: 'Titolo lungo con due punti: il gancio (e una parentesi ironica)'
headline: 'Titolo breve da biglietto, 3-6 parole'
description: 'Una o due frasi: la data, il fatto, la curiosità. Max ~200 caratteri.'
date: 'AAAA-MM-GG'          # il giorno dell'anniversario
categories:
- storie
tags:                         # slug minuscoli con trattini: artista, band, dischi, persone
- nome-artista
cover: /images/articoli/<slug>/<file>.jpg
coverAlt: 'Descrizione visiva della foto, per chi non la vede.'
coverCredit: '<Soggetto>, <luogo>, <data>. Foto di <Autore> via Wikimedia Commons (<licenza>)'
ascolto:
  titolo: 'Titolo disco (anno)'
  nota: 'Una frase su perché ascoltarlo.'
  link: 'https://open.spotify.com/album/…'
draft: false
```

Slug: il nome del file, minuscolo, senza accenti, con trattini (es. `bill-wyman-90-anni`).

## Immagini

- Fonte: **Wikimedia Commons** (o pubblico dominio). Solo licenze che permettono il riuso:
  CC0, pubblico dominio, CC BY, CC BY-SA (con versione e eventuale porting, es. «CC BY-SA 2.0 FR»).
  **Mai** NC (non commerciale), ND (non opere derivate), «fair use» o foto di agenzia.
- Percorso: `public/images/articoli/<slug>/<nome-descrittivo>.jpg`.
- Didascalia/credito: `<Chi/cosa>, <dove>, <quando>. Foto di <Autore> via Wikimedia Commons (<licenza>)`.
- Una foto di copertina + 2-3 in galleria.

## Social (gestiti da Marco con Make)

Per ogni articolo esiste `testi-social/social-<tema>.md` con Facebook, caption Instagram,
primo commento Instagram. Le grafiche si generano con `scripts/social/` (vedi il suo LEGGIMI).
La storia Instagram la pubblica Marco a mano.
