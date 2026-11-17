# Immagini degli articoli (manifest)

Il connettore GitHub degli agenti scrive solo file di testo. Le immagini arrivano così:

1. L'agente (Fotografo) scrive `scripts/immagini/<slug>.json` sul ramo `claude/<slug>`:

```json
{
  "slug": "jeff-buckley-60-anni",
  "immagini": [
    {
      "file": "public/images/articoli/jeff-buckley-60-anni/wolf-river-harbor-memphis.jpg",
      "url": "https://live.staticflickr.com/191/454797575_c8f75f0fda_b.jpg"
    },
    {
      "file": "public/images/articoli/jeff-buckley-60-anni/grace-copertina-album.jpg",
      "url": "https://i.scdn.co/image/ab67616d0000b273afc2d1d2c8703a10aeded0af",
      "lato_max": 640
    }
  ],
  "grafiche": "scripts/social/dati/jeff-buckley-60-anni.json"
}
```

   - `file`: sempre dentro `public/images/articoli/<slug>/`, estensione `.jpg`.
   - `url`: indirizzo diretto dell'immagine. Fonti ammesse: Wikimedia Commons
     (`https://commons.wikimedia.org/wiki/Special:FilePath/<NomeFile>?width=1600` o `upload.wikimedia.org`),
     Flickr (`live.staticflickr.com`, la versione `_b` o `_h`), copertine Spotify (`i.scdn.co`).
     Licenza e credito si verificano **prima**, come da §7 del workflow: il manifest non li controlla.
   - `lato_max` (facoltativo, di default 1600) e `sostituisci: true` per riscaricare un file già presente.
   - `grafiche` (facoltativo): il JSON delle grafiche social da rigenerare dopo le immagini.

2. L'azione «Immagini e grafiche (rami claude)» (`.github/workflows/immagini-e-grafiche.yml`)
   parte da sola: scarica, controlla che siano immagini vere, ridimensiona (max 1600 px, sotto i
   500 KB), genera le grafiche e fa il commit sullo stesso ramo.

3. Dopo qualche minuto l'agente legge `scripts/immagini/<slug>.esito.md` con il connettore
   (`get_file_contents` sul ramo): per ogni file «ok» con dimensioni e peso, oppure l'errore.
   Se qualcosa è andato storto corregge il manifest (o l'URL) e lo salva di nuovo: l'azione riparte.

Le foto che Marco manda a mano si caricano dal browser sul ramo («Add file → Upload files»)
nella cartella `public/images/articoli/<slug>/`; l'azione non le tocca (salvo `sostituisci: true`).
