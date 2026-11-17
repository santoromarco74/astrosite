#!/usr/bin/env python3
"""Scarica e prepara le immagini degli articoli, poi indica quali grafiche social rigenerare.

Usato dall'azione «Immagini e grafiche» (.github/workflows/immagini-e-grafiche.yml) sui rami
claude/**: gli agenti scrivono testi e manifest con il connettore GitHub (che non carica file
binari), questa azione scarica le foto, le ridimensiona e genera le grafiche.

Uso:  python3 scripts/immagini/prepara.py <file con l'elenco dei percorsi cambiati>
Scrive: /tmp/grafiche.txt (un JSON di scripts/social/dati per riga) e
        scripts/immagini/<slug>.esito.md (resoconto leggibile dagli agenti con il connettore).
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

UA = "LaMusicaDelSantoBot/1.0 (https://lamusicadelsanto.it)"
# Flickr ha risposto 403 allo user agent del bot (prova del 17/11/2026): per i suoi server se ne usa uno da browser.
UA_FLICKR = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
# Solo fonti ammesse dal workflow (§7): Commons, Flickr, copertine Spotify.
HOST_AMMESSI = {
    "upload.wikimedia.org", "commons.wikimedia.org", "thumb.wikimedia.org",
    "live.staticflickr.com", "farm1.staticflickr.com", "farm2.staticflickr.com",
    "farm3.staticflickr.com", "farm4.staticflickr.com", "farm5.staticflickr.com",
    "farm6.staticflickr.com", "farm7.staticflickr.com", "farm8.staticflickr.com",
    "farm9.staticflickr.com", "farm66.staticflickr.com",
    "i.scdn.co", "image-cdn-ak.spotifycdn.com", "image-cdn-fa.spotifycdn.com",
}
PESO_MAX = 500_000


def scarica(url):
    host = urllib.parse.urlparse(url).hostname or ""
    if host not in HOST_AMMESSI:
        raise ValueError(f"fonte non ammessa: {host}")
    ultimo = None
    for tentativo in range(4):
        try:
            ua = UA_FLICKR if host.endswith("staticflickr.com") else UA
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=60) as r:
                finale = urllib.parse.urlparse(r.geturl()).hostname or ""
                if finale not in HOST_AMMESSI:
                    raise ValueError(f"reindirizzato verso una fonte non ammessa: {finale}")
                return r.read()
        except ValueError:
            raise
        except Exception as e:  # 429 e simili: si riprova con pause crescenti
            ultimo = e
            time.sleep(15 * (tentativo + 1))
    raise RuntimeError(f"download non riuscito: {ultimo}")


def salva(dati, destinazione, lato_max):
    im = Image.open(io.BytesIO(dati))
    im.load()
    im = im.convert("RGB")
    im.thumbnail((lato_max, lato_max))
    os.makedirs(os.path.dirname(destinazione), exist_ok=True)
    q = 88
    while True:
        im.save(destinazione, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(destinazione) <= PESO_MAX or q <= 55:
            break
        q -= 5
    return im.size, os.path.getsize(destinazione)


def elabora_manifest(percorso, grafiche):
    m = json.load(open(percorso, encoding="utf-8"))
    slug = m["slug"]
    cartella = f"public/images/articoli/{slug}/"
    righe = [f"# Esito immagini per {slug}", "", "| File | Esito |", "|---|---|"]
    cambiato = False
    for img in m.get("immagini", []):
        dest = img["file"]
        if not dest.startswith(cartella) or ".." in dest or not dest.lower().endswith(".jpg"):
            righe.append(f"| `{dest}` | ERRORE: il file deve stare in `{cartella}` e finire in .jpg |")
            continue
        if os.path.exists(dest) and not img.get("sostituisci"):
            righe.append(f"| `{dest}` | già presente, lasciato com'è |")
            continue
        try:
            dim, peso = salva(scarica(img["url"]), dest, int(img.get("lato_max", 1600)))
            righe.append(f"| `{dest}` | ok, {dim[0]}×{dim[1]} px, {peso // 1024} KB |")
            cambiato = True
        except Exception as e:
            righe.append(f"| `{dest}` | ERRORE: {e} |")
        time.sleep(3)  # una richiesta alla volta, con pause
    g = m.get("grafiche")
    if g and (cambiato or not os.path.exists(f"public/social/{slug}-ig.jpg")):
        grafiche.add(g)
    righe += ["", f"Grafiche da rigenerare: {g if g in grafiche else 'nessuna'}"]
    open(f"scripts/immagini/{slug}.esito.md", "w", encoding="utf-8").write("\n".join(righe) + "\n")
    print("\n".join(righe))


def main():
    cambiati = [r.strip() for r in open(sys.argv[1], encoding="utf-8") if r.strip()]
    grafiche = set()
    manifest = {c for c in cambiati if c.startswith("scripts/immagini/") and c.endswith(".json")}
    # Un JSON delle grafiche cambiato: rigenero quelle grafiche (e il suo manifest, se c'è).
    for c in cambiati:
        if c.startswith("scripts/social/dati/") and c.endswith(".json") and os.path.exists(c):
            grafiche.add(c)
    for p in sorted(manifest):
        if os.path.exists(p):
            elabora_manifest(p, grafiche)
    validi = []
    for g in sorted(grafiche):
        foto = json.load(open(g, encoding="utf-8")).get("foto", "")
        if foto and os.path.exists(foto):
            validi.append(g)
        else:
            print(f"Grafiche saltate per {g}: la foto {foto!r} non c'è ancora")
    open("/tmp/grafiche.txt", "w").write("\n".join(validi) + ("\n" if validi else ""))


if __name__ == "__main__":
    main()
