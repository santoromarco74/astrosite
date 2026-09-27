# La musica del Santo — sito Astro

Sito statico di lamusicadelsanto.it, migrato da WordPress (32 articoli, 2 pagine, 225 immagini, stessi indirizzi).

## Struttura
- `src/content/articoli/*.md` — un file per articolo (frontmatter + testo Markdown)
- `src/content/pagine/*.md` — pagine fisse (Chi sono, Privacy)
- `public/wp-content/uploads/` — immagini, stesso percorso di WordPress (i vecchi link continuano a funzionare)
- `src/styles/global.css` — tema "giornale d'epoca" (stile E2b2)
- `keystatic.config.ts` — editor visuale
- `_wp/migrate.py` — script di migrazione (riutilizzabile)

## Comandi
```
npm install
npm run dev      # sito su http://localhost:4321  —  editor su http://localhost:4321/keystatic
npm run build    # genera il sito in dist/
```

## Scrivere un articolo
- Dall'editor: `npm run dev` → /keystatic → Articoli → Nuovo. Salva il file in `src/content/articoli/`.
- A mano: copia un file `.md` esistente e cambia frontmatter e testo.
- `draft: true` nel frontmatter = bozza, non viene pubblicata.
- Immagine con didascalia: `![testo alternativo](/percorso.jpg "Didascalia")`
- Più immagini nello stesso paragrafo (una per riga) = galleria.
- Un link YouTube o Spotify da solo su una riga = player incorporato.

## Messa online (una volta sola)
1. Crea un repository GitHub (es. `lamusicadelsanto`) e carica questa cartella.
2. Collega il repository a Netlify o Cloudflare Pages: build `npm run build`, cartella `dist`.
3. Verifica l'anteprima, poi sposta il dominio lamusicadelsanto.it sul nuovo hosting.
4. (Facoltativo) Editor online: in `keystatic.config.ts` passa a `storage: { kind: 'github', repo: 'UTENTE/lamusicadelsanto' }` e aggiungi l'adapter del tuo hosting.

`public/_redirects` gestisce /feed/ → /rss.xml e i vecchi indirizzi /category/...
