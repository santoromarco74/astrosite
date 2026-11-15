# Redazione

Il flusso di lavoro degli articoli, con gli agenti che fanno la parte meccanica
e Marco che decide.

```
Calendario (lunedì, automatico) ──► Marco sceglie il tema ──► Ricercatore ──► scheda + PR in bozza
                                                                              │
                                              Marco scrive / approva ◄────────┘ ──► merge = pubblicazione
```

## 1. Calendario
- Gira da solo **ogni lunedì mattina** (attività pianificata su claude.ai) e propone 4-5 temi
  per le 4 settimane successive.
- A richiesta: in Claude Code, `usa l'agente calendario` (o in chat: «proponimi dei temi»).

## 2. Ricercatore
- Dopo la scelta: «usa l'agente ricercatore su <tema, data>».
- Produce `redazione/schede/<slug>.md` sul branch `articolo/<slug>` e apre una PR in bozza.

## Cartelle
- `guida-stile.md` — il modo di scrivere del blog. Tienila aggiornata quando cambi stile.
- `schede/` — una scheda di ricerca per articolo.
- `calendario/` — proposte salvate, se vuoi tenerle.

Queste cartelle non finiscono sul sito: Astro pubblica solo `src/` e `public/`.
