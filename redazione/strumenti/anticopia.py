#!/usr/bin/env python3
"""Controllo anti-copia della redazione de La musica del Santo.

Confronta un articolo con i testi delle fonti e segnala le sequenze di N parole
consecutive (predefinito 6) uguali nei due testi. Non fa traduzioni: per le fonti in
inglese il revisore deve comunque controllare a occhio le frasi tradotte alla lettera.

Uso:
  python3 redazione/strumenti/anticopia.py src/content/articoli/<slug>.md fonte1.html fonte2.txt ...
  python3 redazione/strumenti/anticopia.py --n 8 articolo.md fonti/*.html

Le fonti si scaricano FUORI dal repository (es. con curl in una cartella temporanea).
Esce con codice 1 se trova sequenze uguali, 0 se il testo è pulito.
"""
import html
import re
import sys
import unicodedata


def testo_pulito(percorso):
    s = open(percorso, encoding="utf-8", errors="ignore").read()
    if percorso.endswith(".md"):
        s = re.sub(r"^---.*?---", " ", s, count=1, flags=re.S)   # frontmatter
        s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)                # immagini
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)            # link: tengo il testo
        s = re.sub(r"https?://\S+", " ", s)
    else:
        s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
        s = re.sub(r"<[^>]+>", " ", s)
        s = html.unescape(s)
    return s


def parole(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'")
    return re.findall(r"[a-z0-9]+", s)


def main(argv):
    n = 6
    if len(argv) > 2 and argv[1] == "--n":
        n = int(argv[2])
        argv = [argv[0]] + argv[3:]
    if len(argv) < 3:
        print(__doc__)
        return 2
    art = parole(testo_pulito(argv[1]))
    trovati = 0
    for fonte in argv[2:]:
        f = parole(testo_pulito(fonte))
        grammi = {tuple(f[i:i + n]) for i in range(len(f) - n + 1)}
        i, uguali = 0, []
        while i <= len(art) - n:
            if tuple(art[i:i + n]) in grammi:
                j = i + n
                while j < len(art) and tuple(art[j - n + 1:j + 1]) in grammi:
                    j += 1
                uguali.append(" ".join(art[i:j]))
                i = j
            else:
                i += 1
        if uguali:
            trovati += len(uguali)
            print(f"\n== {fonte}: {len(uguali)} sequenze di almeno {n} parole uguali")
            for u in uguali:
                print("  -", u)
    if trovati == 0:
        print(f"Nessuna sequenza di {n} parole in comune con le fonti.")
        return 0
    print("\nNomi propri, titoli e citazioni attribuite tra «» sono ammessi: tutto il resto va riscritto.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
