# La musica del Santo — note per Claude

Sito statico Astro di lamusicadelsanto.it («Guida semiseria per autostoppisti musicali»),
autore Marco Santoro. Dettagli tecnici nel `README.md`.

## Regola d'oro

**Un push su `main` pubblica il sito** (workflow `.github/workflows/deploy-vhosting.yml`,
caricamento FTP a specchio). Non fare mai commit o push diretti su `main`: lavora su un branch
e apri una pull request. Il merge lo fa Marco.

## Dove stanno le cose

- Articoli: `src/content/articoli/<slug>.md` (schema in `src/content.config.ts`)
- Immagini articoli: `public/images/articoli/<slug>/`
- Testi social: `testi-social/social-<tema>.md`; grafiche: `scripts/social/` (vedi LEGGIMI)
- Redazione: `redazione/` — guida di stile, schede di ricerca, proposte del calendario

## Redazione (agenti)

| Agente | File | Cosa fa |
|---|---|---|
| Calendario | `.claude/agents/calendario.md` | Propone 4-5 temi da anniversari verificati |
| Ricercatore | `.claude/agents/ricercatore.md` | Scheda di ricerca con fonti e foto per il tema scelto |

Tutti seguono `redazione/guida-stile.md`. Marco sceglie i temi, scrive o approva i testi e pubblica.
Nessun agente inventa fatti: ciò che non è verificato va dichiarato come tale.
