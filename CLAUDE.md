# La musica del Santo — note per Claude

Sito statico Astro di lamusicadelsanto.it («Guida semiseria per autostoppisti musicali»),
autore Marco Santoro. Dettagli tecnici nel `README.md`.

## Regola d'oro

**Un push su `main` pubblica il sito** (workflow `.github/workflows/deploy-vhosting.yml`,
caricamento FTP a specchio). Non fare mai commit o push diretti su `main`: lavora su un ramo
`claude/<slug>` e apri una pull request. Il merge lo fa Marco.

## Prima di qualsiasi lavoro di redazione

Leggi **`redazione/WORKFLOW.md`**: è l'unico punto in cui è descritto come si lavora (fasi,
agenti, attività programmate, foto, social, newsletter, manutenzione). Per la scrittura vale
**`redazione/guida-stile.md`**. Non duplicare quelle regole altrove: se cambiano, si cambiano lì.

## Dove stanno le cose

- Articoli: `src/content/articoli/<slug>.md` (schema in `src/content.config.ts`)
- Immagini articoli: `public/images/articoli/<slug>/`
- Schede di ricerca: `redazione/schede/<slug>.md`
- Testi social: `testi-social/social-<slug>.md`; grafiche: `scripts/social/` (vedi LEGGIMI)
- Agenti: `.claude/agents/` — calendario, ricercatore, fotografo, redattore, grafico, revisore

Nessun agente inventa fatti: ciò che non è verificato va dichiarato come tale.
