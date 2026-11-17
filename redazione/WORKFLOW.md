# Workflow della redazione — La musica del Santo

**Questo è l'unico punto di riferimento** per come si lavora su lamusicadelsanto.it: persone,
agenti, attività programmate, regole. Se una regola cambia, si cambia **qui** (con una pull
request) e in nessun altro posto. Prompt delle attività programmate, `CLAUDE.md`, doc del
Project di Claude: sono solo rimandi a questo file.

| Cosa | Dove |
|---|---|
| Come si lavora (questo file) | `redazione/WORKFLOW.md` |
| Come si scrive | `redazione/guida-stile.md` |
| Istruzioni di ogni agente | `.claude/agents/<nome>.md` |
| Come si generano le grafiche | `scripts/social/LEGGIMI.md` |
| Note tecniche del sito | `README.md` |
| Dati riservati (accessi FTP, ID di Make, scadenze delle connessioni) | doc `claude/workflow-pubblicazione.md` nel Project di Claude — **mai** nel repository |

Se due documenti si contraddicono, vale questo file; poi si corregge l'altro.

---

## 1. Regole d'oro

1. **Un push su `main` pubblica il sito.** Nessun agente fa commit o push su `main`: si lavora
   su un ramo `claude/<slug>` nuovo (mai riusare rami vecchi) e si apre una pull request.
   Il merge lo fa solo Marco.
2. **Il merge vale come ok per i social** (decisione di Marco, 01/11/2026): il giorno di uscita
   alle 19 i post Facebook e Instagram partono da soli, se l'articolo è online.
   Nient'altro viene pubblicato fuori da questo flusso.
3. **Non si inventa nulla.** Ogni data e ogni fatto vanno letti in una fonte aperta davvero.
   Ciò che non è verificato si scarta o si dichiara «non verificato».
4. **Si scrive in italiano**, con le regole di `redazione/guida-stile.md` (date assolute,
   niente testi di canzoni, titoli senza «Nasce…»).
5. **Marco decide**: sceglie i temi, approva con il merge, può sempre dire «scrivo io».

---

## 2. Chi fa cosa

### Agenti (file in `.claude/agents/`)

| Agente | Quando | Consegna |
|---|---|---|
| **Caporedattore** | È la sessione principale: coordina gli altri e parla con Marco | Proposte, pull request, messaggi |
| **Calendario** | Lunedì (Fase 1) o a richiesta | Proposte della settimana + riserva + «in arrivo» |
| **Ricercatore** | Primo passo della Fase 2 | `redazione/schede/<slug>.md` |
| **Fotografo** | Fase 2, in parallelo al Ricercatore | Copertina + galleria in `public/images/articoli/<slug>/` |
| **Redattore** | Fase 2, dopo scheda e foto | Articolo + `testi-social/social-<slug>.md` |
| **Grafico** | Fase 2, dopo l'articolo | `scripts/social/dati/<slug>.json` + grafiche in `public/social/` |
| **Revisore** | Fase 2, alla fine, senza aver visto il lavoro | Elenco dei problemi |

Il caporedattore avvia ogni agente con lo strumento Agent. Se il tipo di agente con quel nome
non è disponibile nella sessione, avvia un agente generico con l'istruzione: «Leggi
`.claude/agents/<nome>.md`, `redazione/WORKFLOW.md` e `redazione/guida-stile.md` nel repository
e segui quel ruolo», aggiungendo tema, slug, ramo e data.

### Attività programmate (su claude.ai)

| Attività | Quando | Cosa fa |
|---|---|---|
| **Musica del Santo - redazione del lunedì** | lunedì 6:30 | Fase 1, poi nella stessa sessione Fase 2 e Fase 3 (con promemoria) |
| **Musica del Santo - newsletter del sabato** | sabato 8:47 | Bozza della lettera Substack (§8) |
| **Musica del Santo - manutenzione mensile** | giorno 1, 8:52 | Link rotti e controlli di sicurezza, solo rapporto (§9) |

I prompt di queste attività sono volutamente corti: dicono di clonare il repository e di
seguire questo file (i testi sono al §11). L'attività «Calendario La musica del Santo» del
lunedì 7:33 è stata assorbita dalla redazione del lunedì (16/11/2026).

---

## 3. La settimana tipo

```
LUN 6:30   Fase 1: proposte ───► Marco sceglie (tema, giorno, «scrivo io» sì/no)
                                   │ se non risponde entro MER 9:00: sceglie il caporedattore
           tre domande a Marco ─► Marco risponde con le sue considerazioni
           Fase 2: scheda + foto (anche prima delle risposte) ─► articolo (solo dopo le risposte)
                   ─► grafiche ─► revisore ─► build ─► pull request
                                   │
           Marco fa il merge ──────► sito online in pochi minuti
GIORNO DI USCITA 18:52  Fase 3: controlli ─► post Facebook + Instagram ─► link della storia a Marco
SAB 8:47   Newsletter: bozza per Substack (la invia Marco per la domenica)
```

---

## 4. Fase 1 — Proposte del lunedì

Agente: **Calendario** (`.claude/agents/calendario.md`).

1. Elenca cosa è già uscito (`src/content/articoli/`) per non riproporlo.
2. Cerca candidati per la **settimana in corso** (da lunedì a domenica): anniversari tondi e
   attualità (uscite degli ultimi 7-10 giorni o della settimana, ristampe, tour in Italia,
   film e documentari musicali, premi, morti recenti). La ricerca è **giorno per giorno**: per
   ognuno dei sette giorni si leggono nati, morti ed eventi (non solo gli anni tondi attesi).
   I grandi classici con anniversario non tondo si segnalano comunque a parte.
3. Sceglie le **tre proposte migliori** (almeno una di attualità, se valida), una **riserva
   Imperdibili** e una sezione **«In arrivo»** con 2-4 date forti delle tre settimane
   successive, così Marco può prenotarle in anticipo.
4. Il caporedattore manda a Marco un messaggio breve, leggibile dal telefono:
   «Proposte per la settimana dal <lunedì> al <domenica>». Per ogni proposta: tipo, data esatta
   con giorno della settimana, di cosa si tratta, 2-3 curiosità verificate, titolo provvisorio,
   sezione, giorno di uscita consigliato, fonte. Poi riserva, «In arrivo» e «Anche questa
   settimana» (classici non tondi o scartati, una riga l'uno). Chiusura:
   «Dimmi quale pubblicare e quando (e se vuoi scriverlo tu). Se non rispondi entro mercoledì
   alle 9, scelgo io la proposta migliore e ti mando le domande.»
5. Subito dopo programma **nella stessa sessione** (`send_later`) un promemoria per mercoledì
   alle 9:00 (Europe/Rome): «Controllo di mercoledì: se Marco non ha scelto, scegli la proposta
   migliore, mandagli le tre domande e prepara scheda e foto seguendo la Fase 2 di
   redazione/WORKFLOW.md; l'articolo si scrive solo dopo le sue risposte». Se Marco
   risponde prima, il promemoria si cancella (`delete_trigger`). **Un solo promemoria**: prima
   di crearlo si controlla con `list_triggers` che non ce ne sia già uno uguale.

**Giorno di uscita**: il giorno dell'anniversario. Se è già passato o è un pezzo di attualità,
il primo giorno utile. Se sceglie il caporedattore il mercoledì: il giorno dell'anniversario se
cade tra giovedì e domenica, altrimenti giovedì.

---

## 5. Fase 2 — Pacchetto

Parte dopo la scelta di Marco (o mercoledì alle 9). Si lavora nel repository clonato, da
`main` aggiornato (`git fetch origin main`), su un ramo nuovo **`claude/<slug>`**.

| Passo | Agente | Risultato |
|---|---|---|
| 0 | Caporedattore | Manda a Marco le **tre domande** (ricordo, opinione, collegamento) e una tesi proposta in una frase |
| 1 | Ricercatore | `redazione/schede/<slug>.md`: fatti con fonte, aneddoti, chicca italiana, link interni ed esterni, video ufficiali, disco «Da ascoltare» |
| 1 (in parallelo) | Fotografo | Copertina + galleria da 3 o 6 foto, con didascalie, crediti, alt e «fuoco» (§7) |
| 2 | Redattore | `src/content/articoli/<slug>.md` + `testi-social/social-<slug>.md` |
| 3 | Grafico | Dati e tre grafiche (Instagram, Facebook, storia) |
| 4 | Revisore | Problemi da correggere, compreso il **controllo anti-copia** con `redazione/strumenti/anticopia.py` sulle fonti principali; se sono molti, secondo passaggio |
| 5 | Caporedattore | `npm ci && npm run build` senza errori; in `dist/` la pagina ha il blocco `class="galleria"` con il numero giusto di foto; commit, push, pull request |

**Fonti**: Wikipedia serve solo per orientarsi. Ogni scheda ha almeno tre fonti indipendenti
non Wikipedia, di cui una primaria e una italiana; l'elenco di dove cercare è in
`.claude/agents/ricercatore.md` («Dove cercare»).

**Le tre domande a Marco** (guida di stile, «Voce unica»): partono subito dopo la scelta, in un
messaggio solo, insieme alla tesi proposta. Ricerca e foto possono partire subito, ma
**l'articolo si scrive solo dopo le risposte di Marco** (decisione di Marco, 17/11/2026): le sue
considerazioni sono il punto di partenza del pezzo, non un'aggiunta. Se le risposte non arrivano,
il caporedattore manda **un solo promemoria** (`send_later`, il giorno dopo alle 9) e, se il giorno
di uscita è troppo vicino per scrivere, propone a Marco una nuova data o la riserva Imperdibili.
Mai scrivere l'articolo senza le risposte. Nelle risposte di Marco non si aggiunge nulla di
inventato.

**Se Marco ha detto «scrivo io»**: ci si ferma dopo il passo 1 (scheda + foto), si apre la pull
request **in bozza** e gli si mandano i 3 fatti più forti e l'angolo consigliato. Quando Marco
ha scritto, a richiesta si riparte dal passo 3.

**Come si scrive sul ramo** (dal 17/11/2026): le sessioni automatiche di Cowork non possono
fare `git push`, ma il **connettore GitHub** può creare il ramo, scrivere file di **testo** e aprire
la pull request (`create_branch`, `push_files` / `create_or_update_file`, `create_pull_request`).
Le **immagini** non passano dal connettore: il Fotografo scrive il manifest
`scripts/immagini/<slug>.json` con gli indirizzi delle foto e l'azione GitHub «Immagini e grafiche
(rami claude)» le scarica, le prepara, genera le tre grafiche social e fa il commit sullo stesso
ramo. Dopo qualche minuto si legge l'esito in `scripts/immagini/<slug>.esito.md` (istruzioni in
`scripts/immagini/LEGGIMI.md`). Ordine: ramo → articolo, scheda, testi social, JSON delle
grafiche e manifest → attesa dell'esito → revisore → pull request. Se anche il connettore non
funziona, si torna alla patch da mandare a Marco. La build di prova (`npm run build`) si fa nel
clone locale della sessione prima di scrivere sul ramo.

**Cosa entra nel ramo**: articolo, immagini, scheda, testi social, dati e file delle grafiche.
Niente patch, zip o cartelle di lavoro. `redazione/` e `testi-social/` non finiscono sul sito
(Astro pubblica solo `src/` e `public/`).

**Pull request** (la GraphQL di `gh` è bloccata nelle sessioni cloud: niente `gh pr create`):

```
gh api repos/santoromarco74/astrosite/pulls -f title="<titolo>" -f head="claude/<slug>" -f base="main" -f body="<descrizione>"
```

Descrizione: argomento, data di uscita, fonti, foto usate con licenza (e link alla pagina di
autorizzazione per le foto stampa), eventuale elenco Depositphotos, dubbi del revisore, testi social.

**Messaggio a Marco**: link della pull request, anteprima Netlify
(`https://claude-<slug>--lamusicadelsanto.netlify.app`, se generata), data di uscita, eventuale
elenco Depositphotos, dubbi rimasti, e la frase: «Fai il merge quando vuoi: il giorno <data>
alle 19 pubblico in automatico su Facebook e Instagram, se l'articolo è online.»

Infine, con `send_later`, promemoria nella stessa sessione per il giorno di uscita alle 18:52
(Europe/Rome): «Pubblicazione social di <slug>: segui la Fase 3 di redazione/WORKFLOW.md».

---

## 6. Fase 3 — Social

1. **Controlli**: la pull request è `merged` (`gh api repos/santoromarco74/astrosite/pulls/<numero>`);
   `https://lamusicadelsanto.it/<slug>/` risponde 200; rispondono 200 anche
   `https://lamusicadelsanto.it/social/<file>-ig.jpg` e `-fb.png`.
2. **Se tutto è a posto**: scenario Make «LMS - Social (Facebook + Instagram)», con i testi di
   `testi-social/social-<slug>.md`. Prima azione `facebook` (testo con il link, `image_url` della
   grafica `-fb.png`), poi azione `instagram` (caption, `image_url` della grafica `-ig.jpg`,
   `commento` «👉 L'articolo completo: lamusicadelsanto.it/<slug>»).
   - Pagina Facebook **solo «La musica del Santo»**, mai «Storie di musica».
   - Instagram accetta solo JPEG.
   - **Ogni post una volta sola**: se una chiamata dà errore non si ripete alla cieca, si
     controlla e si riferisce.
3. **Messaggio a Marco**: conferma dei due post e link della storia
   `https://lamusicadelsanto.it/social/<file>-storia.jpg`, da caricare dall'app con lo sticker
   Link all'articolo (Make non pubblica storie).
4. **Se manca il merge o la pagina non è online**: una riga a Marco e nuovo controllo il giorno
   dopo alle 18:52. Al massimo 3 rinvii, poi ci si ferma e si chiede a Marco.

---

## 7. Foto e immagini

Ogni articolo ha una **copertina** (usata anche nelle grafiche) e, se possibile, una
**galleria di 3 oppure 6 foto** (la griglia è a 3 colonne): diverse dalla copertina e tra loro.
Con 3, 4 o 5 foto valide se ne usano 3; con 6 o più le 6 migliori; con meno di 3 niente galleria.

**Licenze ammesse**: CC BY, CC BY-SA, CC0, pubblico dominio. Mai NC o ND, mai fotogrammi,
foto di agenzia (Getty, AP, Reuters…) o immagini senza licenza chiara. La licenza si legge
sulla pagina del file, non si deduce.

**Fonti, in quest'ordine** (si passa alla successiva solo se la precedente non basta):

1. **Wikimedia Commons** tramite API, sempre con
   `curl -A "LaMusicaDelSantoBot/1.0 (https://lamusicadelsanto.it)"` (senza user agent risponde 429):
   `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=<termini>&gsrnamespace=6&gsrlimit=30&prop=imageinfo&iiprop=url|size|extmetadata&iiextmetadatafilter=LicenseShortName|Artist|Credit|DateTimeOriginal|ImageDescription&format=json`
   (e le categorie Commons dell'artista). Download:
   `https://commons.wikimedia.org/wiki/Special:FilePath/<NomeFile>?width=1600`, una richiesta
   alla volta con qualche secondo di pausa; dopo ogni download `file` per controllare che sia
   un'immagine.
2. **Flickr tramite Openverse** (gratuito, senza chiave):
   `https://api.openverse.org/v1/images/?q=<termini>&license=by,by-sa,cc0,pdm&source=flickr&page_size=20`.
   Prima di usare una foto si apre `foreign_landing_url` e si conferma che la licenza sia ancora
   quella. Credito: «Foto di <creator> via Flickr (CC <licenza> <versione>)».
3. **Foto stampa ufficiali**: solo dalla sezione stampa del sito ufficiale di artista, etichetta
   o ufficio stampa, e solo se la pagina autorizza esplicitamente l'uso editoriale. Credito come
   indicato lì + «foto stampa ufficiale»; link della pagina nella pull request.
4. **Foto di Marco** (Depositphotos con il suo abbonamento, o foto che manda lui): **solo se
   le fonti 1-3 non bastano**. Le cercano sempre prima gli agenti; a Marco si chiede solo ciò che
   manca, con un elenco preciso (soggetto, periodo, 2-3 parole chiave in inglese, dove va, quale
   foto sostituirebbe) nella pull request e nel messaggio. Marco le carica sul ramo dal browser
   o le manda in chat. Didascalia «Foto Depositphotos» o il credito che indica lui. La pull
   request non aspetta queste foto.
5. **Illustrazione originale**, solo per la copertina e solo se non c'è altro (o il tema è un
   luogo o un'idea): disegnata in codice con colori e caratteri del sito. Oggetti e simboli;
   **mai** persone reali, copertine, loghi, marchi o personaggi protetti. Credito
   «Illustrazione di La musica del Santo».

**Copertine dei dischi** (decisione di Marco, 05/11/2026): solo quando quel disco è il tema
dell'articolo o del passaggio (articolo su un album, Imperdibili, storia di una copertina).
Se l'articolo è sull'album, la copertina del disco è la copertina dell'articolo; altrimenti va
nel testo accanto al passaggio. Mai per decorare, mai mescolate alla galleria di foto.
Fonte: Spotify a 640 px — dall'oembed dell'album
(`https://open.spotify.com/oembed?url=https://open.spotify.com/album/<id>`) si prende il codice
finale di `thumbnail_url` e si scarica `https://i.scdn.co/image/ab67616d0000b273<codice>`;
si guarda l'immagine (deve essere l'originale, non un'edizione deluxe con scritte).
Didascalia: «La copertina di «<titolo>» di <artista> (<anno>). © dei titolari dei diritti,
riprodotta per critica e discussione».

**File**: `public/images/articoli/<slug>/<nome-descrittivo>.jpg`, lato lungo massimo 1600 px,
sotto i 500 KB; almeno 1200 px sul lato corto per la copertina, 800 px per la galleria.
**Didascalia**: soggetto e anno, autore, fonte, licenza — es. «Bill Wyman nel 1989. Foto di
Gorup de Besanez via Wikimedia Commons (CC BY-SA 4.0)».

**Riquadro «Da ascoltare»**: il link porta sempre all'album su Spotify
(`https://open.spotify.com/album/<id>`), verificato con l'oembed (il titolo deve essere
l'album giusto, non un singolo o un remix).

---

## 8. Newsletter del sabato

Solo **bozza**: non si pubblica nulla, non si usa Make, non si tocca il repository.
Su Substack la lettera la incolla e la invia Marco.

1. Raccogli gli articoli usciti negli ultimi 7 giorni (dal sabato precedente al venerdì
   compreso) da `https://lamusicadelsanto.it/rss.xml` e dalla sitemap. Leggili davvero.
2. Struttura fissa della lettera:
   - **Oggetto**: «N. <numero> — <titolo breve>». Il N. 1 è uscito domenica 8 novembre 2026:
     si contano le domeniche da allora (15 novembre 2026 = N. 2, 22 novembre 2026 = N. 3…),
     controllando la coerenza con l'ultima bozza `claude/newsletter_*.md` del Project.
   - **Sottotitolo**: una riga.
   - **Apertura**: 2-3 righe nel tono del blog + segnaposto «[Qui una riga tua sulla settimana]».
     Mai inventare esperienze o opinioni di Marco.
   - **Gli articoli della settimana**: titolo in grassetto, due righe scritte apposta (non il
     sommario del sito), link «Leggi la storia →».
   - **Se ve lo siete persi**: un articolo d'archivio legato alla settimana o a un anniversario
     vicino, mai già usato nelle newsletter precedenti.
   - **Il disco della settimana**: anno, una riga sul perché + «[Una riga tua su questo disco]».
   - **La domanda** ai lettori, con invito a rispondere all'email.
   - **Chiusura**: «A domenica prossima,\nMarco» e il P.S. «Se la lettera vi è piaciuta,
     inoltratela a un amico che ascolta bella musica.»
3. Valgono le regole di `guida-stile.md` (date assolute, niente testi di canzoni); ogni fatto
   aggiunto rispetto agli articoli va verificato, altrimenti non si scrive.
4. Se in settimana non è uscito nulla: dirlo in una riga e fare una lettera breve con due
   pezzi d'archivio e il disco della settimana.
5. Salva la bozza nel Project come `claude/newsletter_n<numero>_<AAAA-MM-GG della domenica>.md`.
6. Un solo messaggio a Marco con la lettera pronta da incollare e in fondo: «Aggiungi le tue
   righe tra parentesi quadre, incolla su Substack e programma l'invio per domenica mattina.»

---

## 9. Manutenzione mensile

Solo **controllare e riferire**: nessuna modifica, niente repository, niente Make.

1. **Link**: dalla sitemap `https://lamusicadelsanto.it/sitemap-0.xml` apri ogni pagina e
   controlla link e immagini. Interni: segnala ogni risposta diversa da 200 (dopo i redirect).
   Esterni: segnala 404, 410 e mancate risposte; ignora 403 e 429 (blocchi anti-bot), salvo una
   riga a parte se sono tanti.
2. **Sicurezza**:
   - `/wp-login.php`, `/xmlrpc.php` e `/wp-admin/` rispondono 410;
   - `http://lamusicadelsanto.it` e `https://www.lamusicadelsanto.it` reindirizzano (301) a
     `https://lamusicadelsanto.it/`;
   - la home ha le intestazioni Strict-Transport-Security, X-Content-Type-Options,
     X-Frame-Options e Referrer-Policy;
   - nessuno script da domini inattesi (attesi: il sito, fonts.googleapis.com/fonts.gstatic.com,
     player YouTube o Spotify);
   - nessun URL `.php` risponde 200.
3. **Scadenze**: leggi nel doc riservato del Project le scadenze delle connessioni Make e
   segnala quelle entro 30 giorni.
4. Un messaggio breve: prima riga «Tutto a posto» oppure «Ci sono N cose da sistemare»; poi i
   problemi (pagina, link o controllo, proposta di correzione in una riga); in fondo solo il
   conteggio di pagine e link controllati.

---

## 10. Note tecniche per gli agenti

- **Sito**: Astro statico. Ogni push su `main` → GitHub Actions «Pubblica su VHosting»
  (`.github/workflows/deploy-vhosting.yml`) → online in pochi minuti. Netlify serve solo per
  le anteprime dei rami. Gli agenti non vedono GitHub Actions: la verifica si fa sul sito.
- **Sezioni** (`categories`): `storie`, `album`, `attualita`, `film`, `imperdibili`.
- **Galleria**: immagini su righe consecutive, una per riga, senza righe vuote in mezzo, con
  una riga vuota prima e dopo. Una sola immagine su una riga = foto con didascalia.
- **Player**: un link YouTube o Spotify da solo su una riga.
- **Grafiche**: `NODE_PATH=$(npm root -g) node scripts/social/genera.cjs scripts/social/dati/<slug>.json`
  → `public/social/<nome>-ig.jpg`, `-fb.png`, `-storia.jpg`. Fascia sempre con data assoluta.
- **GitHub**: nelle sessioni di Cowork si scrive con il connettore GitHub (solo testo) e le
  immagini passano dal manifest e dall'azione «Immagini e grafiche» (§5). Dove `git push`
  funziona, push dei rami e pull request con `gh api` (REST). Niente `gh pr create`, niente
  cancellazione di rami remoti, niente push su `main`.
- **Wikipedia**: dalle sessioni cloud lo strumento di lettura delle pagine può essere bloccato.
  In quel caso si usano le API con `curl` e lo user agent del §7, oppure altre fonti aperte.
  Una data non letta in nessuna fonte non si usa.
- **Messaggi a Marco**: brevi, leggibili dal telefono; nelle sessioni automatiche anche con
  la notifica.

---

## 11. Prompt delle attività programmate

Testo di riferimento: se si cambia un'attività su claude.ai, si aggiorna anche qui.

**Redazione del lunedì**
> Sei il caporedattore AI di lamusicadelsanto.it, il blog musicale di Marco. Scrivi sempre in
> italiano. Clona https://github.com/santoromarco74/astrosite e leggi `redazione/WORKFLOW.md`,
> `redazione/guida-stile.md` e `.claude/agents/`. Esegui la Fase 1 (proposte del lunedì) e poi,
> in questa stessa sessione, le Fasi 2 e 3 come descritto lì, coordinando gli agenti con lo
> strumento Agent. Mai commit o push su `main`; non pubblicare nulla fuori da quel flusso; non
> inventare nulla. Se non riesci a leggere quei file, fermati e avvisa Marco.

**Newsletter del sabato**
> Sei l'autore AI della newsletter «La musica del Santo» (Substack). Scrivi sempre in italiano.
> Clona https://github.com/santoromarco74/astrosite in sola lettura e segui il §8 di
> `redazione/WORKFLOW.md` e `redazione/guida-stile.md`. Prepari solo la bozza: non pubblicare
> nulla, non usare Make, non modificare il repository. Se non riesci a leggere quei file,
> fermati e avvisa Marco.

**Manutenzione mensile**
> Sei il manutentore di lamusicadelsanto.it. Scrivi sempre in italiano. Clona
> https://github.com/santoromarco74/astrosite in sola lettura e segui il §9 di
> `redazione/WORKFLOW.md`. Solo controllare e riferire: non modificare nulla, non usare Make,
> non pubblicare nulla. Se non riesci a leggere quel file, fermati e avvisa Marco.

---

## 12. Registro delle decisioni

| Data | Decisione |
|---|---|
| 29/09/2026 | Niente riferimenti temporali relativi: sempre date assolute |
| 23/10/2026 | WordPress dismesso; sito statico Astro pubblicato su VHosting a ogni push su `main` |
| 01/11/2026 | Il merge della pull request vale come ok per i post Facebook e Instagram |
| 05/11/2026 | Copertine dei dischi solo dove il disco è il tema, da Spotify a 640 px |
| 06/11/2026 | Ordine delle fonti foto: Commons → Openverse/Flickr → foto stampa → Depositphotos → illustrazione |
| 17/11/2026 | L'articolo si scrive solo dopo le risposte di Marco alle tre domande; le foto le propone Marco solo se gli agenti non ne trovano di disponibili |
| 17/11/2026 | Scrittura sui rami con il connettore GitHub (testo) e immagini/grafiche preparate dall'azione «Immagini e grafiche (rami claude)» a partire dal manifest `scripts/immagini/<slug>.json` |
| 17/11/2026 | Fonti: Wikipedia solo per orientarsi; per ogni scheda almeno tre fonti non Wikipedia, di cui una primaria e una italiana (elenco nel file del Ricercatore) |
| 17/11/2026 | Voce unica: una tesi per pezzo, mai l'ordine delle fonti, tre domande a Marco prima di scrivere, al massimo una formula fissa, controllo anti-copia con `redazione/strumenti/anticopia.py`. Dopo aver trovato un sito con un pezzo sui Beastie Boys quasi uguale al nostro. Solo per i nuovi articoli |
| 16/11/2026 | Calendario: ricerca obbligatoria giorno per giorno (nati, morti, eventi) e segnalazione dei classici non tondi, dopo che erano sfuggiti i 60 anni di Jeff Buckley (17/11) e il «White Album» (22/11) |
| 16/11/2026 | Workflow in un unico punto (questo file). Una sola attività del lunedì (proposte della settimana + riserva + «in arrivo»). Dopo la scelta: scheda di ricerca e poi pacchetto completo, salvo «scrivo io». Un solo tipo di ramo: `claude/<slug>`. Testi social in `testi-social/` |
