#!/usr/bin/env python3
"""Elenchi «giorno per giorno» per il Calendario de La musica del Santo.

Scarica le pagine del giorno di Wikipedia in italiano e in inglese (eventi, nati, morti),
tiene solo le righe che parlano di musica e calcola gli anni trascorsi. Così l'agente
non legge le pagine una per una: legge un solo file e sceglie.

Uso:
  python3 redazione/strumenti/giorni.py 2026-11-16 2026-11-22 > /tmp/giorni.md

Una richiesta alla volta, con pausa, e nuovi tentativi se Wikipedia risponde 429.
Le pagine non lette finiscono in fondo al file: quei giorni vanno coperti con un'altra fonte.
Le date restano da verificare su una fonte aperta non Wikipedia prima di proporle.
"""
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "LaMusicaDelSantoBot/1.0 (https://lamusicadelsanto.it)"
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
PAROLE = re.compile(
    r"cantant|musicist|composit|chitarrist|batterist|bassist|tastierist|cantautor|"
    r"pianist|rapper|\bband\b|gruppo musicale|\balbum|\bsingol|\bdisco\b|\bconcerto|festival musicale|"
    r"\bjazz|\brock\b|\bsoul\b|\bblues|\bopera\b|orchestra|direttore d'orchestra|produttore discografico|"
    r"singer|musician|composer|guitarist|drummer|bassist|keyboardist|songwriter|pianist|"
    r"record producer|\bDJ\b|released|rock and roll|hip hop|Beatles|Rolling Stones",
    re.I)
TONDI = {10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100}


def wikitext(lingua, pagina):
    url = (f"https://{lingua}.wikipedia.org/w/api.php?action=parse&format=json&prop=wikitext"
           f"&formatversion=2&page={urllib.parse.quote(pagina)}")
    for tentativo in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)["parse"]["wikitext"]
        except Exception:  # 429, rete, pagina mancante
            time.sleep(5 * (tentativo + 1))
    return None


def pulisci(riga):
    riga = re.sub(r"<ref[^>]*/>|<ref.*?</ref>", "", riga)
    riga = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", riga)
    riga = re.sub(r"\{\{[^}]*\}\}", "", riga)
    riga = re.sub(r"'{2,}", "", html.unescape(riga))
    riga = re.sub(r"<[^>]+>.*?</[^>]+>|<[^>]+>", "", riga)
    return re.sub(r"\s+", " ", riga).strip(" *:-–")


def righe_musica(testo, anno_corrente):
    sezione, uscita = "?", []
    for riga in testo.splitlines():
        t = re.match(r"^==\s*([^=].*?)\s*==$", riga)  # solo i titoli di secondo livello
        if t:
            sezione = pulisci(t.group(1))
            continue
        if not riga.startswith("*") or not PAROLE.search(riga):
            continue
        r = pulisci(riga)
        a = re.match(r"^(\d{3,4})", r)
        anni = anno_corrente - int(a.group(1)) if a else None
        segno = " ★" if anni in TONDI else ""
        uscita.append(f"- [{sezione}] {r}" + (f" — {anni} anni{segno}" if anni is not None else ""))
    return uscita


def main():
    inizio = dt.date.fromisoformat(sys.argv[1])
    fine = dt.date.fromisoformat(sys.argv[2])
    non_letti = []
    giorno = inizio
    while giorno <= fine:
        print(f"\n## {giorno.isoformat()}\n")
        data_it = f"{giorno.day}_{MESI[giorno.month - 1]}"
        for lingua, pagina in (("it", data_it), ("it", f"Nati_il_{data_it}"),
                               ("it", f"Morti_il_{data_it}"),
                               ("en", f"{MONTHS[giorno.month - 1]}_{giorno.day}")):
            testo = wikitext(lingua, pagina)
            time.sleep(2)
            if testo is None:
                non_letti.append(f"{giorno.isoformat()} ({lingua}: {pagina})")
                continue
            righe = righe_musica(testo, giorno.year)
            print(f"### {lingua}: {pagina} ({len(righe)} righe di musica)\n")
            print("\n".join(righe) or "- nessuna")
        giorno += dt.timedelta(days=1)
    print("\n## Pagine NON LETTE (da coprire con un'altra fonte)\n")
    print("\n".join(f"- {g}" for g in non_letti) or "- nessuno")


if __name__ == "__main__":
    main()
