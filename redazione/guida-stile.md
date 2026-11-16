# Guida di stile — La musica del Santo

Ricavata dagli articoli pubblicati tra settembre e novembre 2026 (Back to Black, Chuck Berry,
Bill Wyman, Leonard Cohen, Led Zeppelin IV, Sting, Atom Heart Mother, l'Olandese Volante).
È l'**unica guida di stile**: vale per articoli, testi social, grafiche e newsletter, e per
tutti gli agenti della redazione (il processo è in `redazione/WORKFLOW.md`). Se un articolo
nuovo di Marco si discosta da qui, ha ragione l'articolo: aggiornate la guida.

## Identità

- Sottotitolo del sito: «Guida semiseria per autostoppisti musicali» (per esteso: «Piccola guida
  semiseria per autostoppisti persi nell'etere musicale»).
- Metafora di casa: il concerto e il biglietto (biglietteria, «in cartellone», «ingresso»).
- Pubblico: appassionati italiani tra i 25 e i 45 anni, non addetti ai lavori. «Bella musica»:
  rock come base, aperti a soul, R&B, jazz, pop, cantautori, elettronica, del passato e del presente.
  Si racconta, non si recensisce.
- Tono: semiserio, caldo, curioso. Mai accademico, mai agiografico («niente santini»).
  Le ombre degli artisti si dicono, «senza giri di parole», ma senza morbosità.
- Da evitare: gergo tecnico non spiegato, esaltazioni («capolavoro assoluto»), stroncature
  fini a se stesse.

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
  pubblicato **il giorno stesso** dell'anniversario (se è già passato, o per l'attualità,
  il primo giorno utile).
- Lunghezza: 950-1.600 parole (lettura 4-6 minuti).

## Struttura tipica

1. **Attacco**: la data e il numero in grassetto nella prima o seconda frase
   («Il **24 ottobre 2026** **Bill Wyman** compie **90 anni**»). Spesso un aggancio al pezzo
   precedente («Dopo i cento anni di Chuck Berry…»).
2. `## Il racconto di …` — le origini, con 1-3 `###` di episodi.
3. `## L'approfondimento: …` — il cuore: come è nato il disco, la svolta, i retroscena.
4. Facoltativo: `## L'eredità …` / una sezione sulle ombre.
5. `## Se dovessi dire cosa rappresenta…` — la sola parte in prima persona singolare, il giudizio.
6. Galleria: **3 oppure 6** immagini, una per riga su righe consecutive, con didascalia e credito.
7. `## Se volete approfondire` — cosa ascoltare/guardare, in che ordine, link a pezzi interni.
8. **Chiusa**: una domanda ai lettori («E voi, qual è la vostra canzone di…?»).

I titoli dei paragrafi sono frasi con un'immagine concreta, non etichette
(«Il concerto in pigiama», «Una casa fredda, un camion e mille sterline a settimana»).

## Titoli

- `title` (pagina e Google): completo e descrittivo, anche lungo.
- `headline` (prima pagina, schede, grafiche): corto, da strillone, massimo ~40 caratteri.
- Titoli originali: **mai** la formula «Nasce …» o «X anni fa nasceva …».

## Date e riferimenti temporali (regola di Marco, 29/09/2026)

Un testo deve restare vero anche letto dopo mesi o anni. Vale per articoli, post, caption,
grafiche e newsletter.

- ❌ Mai: «ieri», «oggi», «domani», «stasera», «qualche giorno fa», «la settimana scorsa»,
  «il mese scorso», «quest'anno», «l'anno scorso», «di recente», «ultimamente», «a breve»,
  «tra poco», «proprio in questi giorni», un giorno della settimana da solo («lunedì»),
  «Accadde oggi».
- ✅ Sempre la **data assoluta** («il 28 settembre 1976», «lunedì 28 settembre 2026»,
  «nel settembre 2026»), oppure il titolo dell'articolo collegato con link interno.
- Il conteggio dell'anniversario («compie 35 anni») è ammesso, ma accanto alla data completa.
- Eventi in corso (tour, uscite, mostre): date esatte, mai «è in corso».
- Restano ammessi i riferimenti al passato storico: «all'epoca», «in quegli anni», «ancora oggi».
- **Nessuna citazione di testi di canzoni.**

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
- **Link esterni**: 3-8 per articolo, solo alla **prima citazione** di artista, disco, brano.
  Wikipedia in italiano (in inglese solo se manca la voce) o il sito ufficiale; fonti autorevoli
  per i fatti discussi. Mai un link su ogni nome.
- **Link interni**: 2-3 per articolo, `[testo](/slug/)` o `/tag/<artista>/`. Se il blog ha già un
  pezzo su quell'artista o disco, si linka quello invece di Wikipedia.
- **YouTube**: solo per i brani di cui si parla davvero e solo da canali ufficiali (artista,
  VEVO, «Topic»). Mai caricamenti amatoriali.
- **Player**: un link Spotify o YouTube da solo su una riga diventa un player incorporato.
  Al massimo 1-2 per articolo.

## Frontmatter

```yaml
title: 'Titolo lungo con due punti: il gancio (e una parentesi ironica)'
headline: 'Titolo breve da biglietto, 3-6 parole'
description: 'Una o due frasi: la data, il fatto, la curiosità. Max ~200 caratteri.'
date: 'AAAA-MM-GG'          # il giorno di uscita (di norma quello dell'anniversario)
categories:
- storie
tags:                         # slug minuscoli con trattini: artista, band, dischi, persone
- nome-artista
cover: /images/articoli/<slug>/<file>.jpg
coverAlt: 'Descrizione visiva della foto, per chi non la vede.'
coverCredit: '<Soggetto> nel <anno>. Foto di <Autore> via Wikimedia Commons (<licenza>)'
ascolto:
  titolo: 'Titolo disco (anno)'
  nota: 'Una frase su perché ascoltarlo.'
  link: 'https://open.spotify.com/album/…'   # sempre l'album su Spotify, verificato
draft: false
```

Slug: il nome del file, minuscolo, senza accenti, con trattini (es. `bill-wyman-90-anni`).

## Immagini

Le regole complete (fonti, licenze, copertine dei dischi, illustrazioni, formati) sono nel
§7 di `redazione/WORKFLOW.md`. In breve:

- Una foto di copertina + una galleria di **3 o 6** foto (oppure nessuna galleria).
- Solo licenze CC BY, CC BY-SA, CC0, pubblico dominio (o foto stampa autorizzate, o Depositphotos
  fornite da Marco). **Mai** NC, ND, fotogrammi, foto di agenzia.
- Copertine dei dischi solo dove il disco è il tema, con la didascalia ©.
- Didascalia con credito completo: «Bill Wyman nel 1989. Foto di Gorup de Besanez via
  Wikimedia Commons (CC BY-SA 4.0)».

## Social

Per ogni articolo esiste `testi-social/social-<slug>.md` con tre parti:

- **Facebook**: tono diretto, una domanda ai lettori, link `https://lamusicadelsanto.it/<slug>/`.
  Emoji con parsimonia (🎵 🎸 💿).
- **Instagram - caption**: più evocativa, chiusa da «link nel primo commento» e dagli hashtag
  `#lamusicadelsanto #anniversario #bellamusica` più quelli pertinenti.
- **Instagram - primo commento**: «👉 L'articolo completo: lamusicadelsanto.it/<slug>».

Anche qui: date assolute, niente testi di canzoni. Le grafiche si generano con `scripts/social/`
(vedi il suo LEGGIMI); la fascia porta sempre una data assoluta («Accadde il 24 ottobre 1936»).
La pubblicazione è descritta nel §6 del workflow; la storia Instagram la carica Marco a mano.

## Controllo finale

- [ ] La data e il numero sono nell'attacco, in grassetto?
- [ ] Almeno 3 aneddoti o curiosità, ognuno con la sua fonte nella scheda?
- [ ] Cercata la chicca italiana?
- [ ] Nessuna parola della lista ❌ sui riferimenti temporali? Nessun testo di canzone?
- [ ] `headline` entro ~40 caratteri, titolo senza «Nasce…»?
- [ ] Link: 3-8 esterni alla prima citazione, 2-3 interni, YouTube solo ufficiali, 1-2 player?
- [ ] Ogni immagine ha licenza verificata e credito completo? Galleria da 3 o 6?
- [ ] «Da ascoltare» porta all'album giusto su Spotify?
- [ ] La chiusa è una domanda ai lettori? Il pezzo «suona» come La musica del Santo?
