"""Migrazione WordPress -> Astro (Markdown + frontmatter).
Legge i JSON scaricati dall'API REST pubblica e scrive:
  src/content/articoli/<slug>.md
  src/content/pagine/<slug>.md
  public/wp-content/uploads/... (immagini, stesso percorso di WordPress)
"""
import json, re, os, html, urllib.request, urllib.parse, yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import MarkdownConverter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP = os.path.dirname(os.path.abspath(__file__))
SITE = "https://lamusicadelsanto.it"
UP = SITE + "/wp-content/uploads/"

def load(n):
    return json.load(open(os.path.join(WP, n)))

posts = load("posts.json"); pages = load("pages.json"); cats = load("cats.json")
tags = []
for i in (1, 2, 3):
    try:
        d = load(f"tags{i}.json")
        if isinstance(d, list): tags += d
    except Exception: pass
media = []
for i in (1, 2, 3):
    d = load(f"media{i}.json")
    if isinstance(d, list): media += d
cat_by_id = {c["id"]: c for c in cats}
tag_by_id = {t["id"]: t for t in tags}
media_by_id = {m["id"]: m for m in media}
media_urls = {m["source_url"] for m in media}

needed_images = set()

SIZE_RE = re.compile(r"-\d+x\d+(?=\.(jpe?g|png|gif|webp)$)", re.I)

def full_image(url):
    """Riporta un'immagine ridimensionata all'originale, se esiste."""
    if not url: return url
    url = html.unescape(url).split("?")[0]
    if url.startswith("//"): url = "https:" + url
    base = SIZE_RE.sub("", url)
    if base in media_urls: return base
    scaled = re.sub(r"(\.\w+)$", r"-scaled\1", base)
    if scaled in media_urls: return scaled
    return url

def local(url):
    """URL assoluto del sito -> percorso relativo."""
    if url.startswith(UP):
        needed_images.add(url)
        return "/wp-content/uploads/" + url[len(UP):]
    if url.startswith(SITE):
        return url[len(SITE):] or "/"
    return url

def clean_text(s):
    return re.sub(r"\s+", " ", s or "").strip()

def youtube_id(src):
    m = re.search(r"youtube(?:-nocookie)?\.com/embed/([\w-]{6,})", src)
    return m.group(1) if m else None

def img_md(img, caption=""):
    a = img.find_parent("a")
    src = img.get("data-src") or img.get("src") or ""
    if a and a.get("href", "").startswith(UP) and re.search(r"\.(jpe?g|png|gif|webp)$", a["href"], re.I):
        src = a["href"]
    src = local(full_image(src))
    alt = clean_text(img.get("alt", "")).replace("[", "(").replace("]", ")")
    cap = clean_text(caption).replace('"', "'")
    return f'![{alt}]({src} "{cap}")' if cap else f"![{alt}]({src})"

def transform(soup):
    # rumore
    for sel in ["style", "script", "noscript", ".rt-reading-time", ".kb-table-of-content-nav",
                ".wp-block-kadence-tableofcontents", ".sharedaddy", ".jp-relatedposts",
                "button", "svg", ".wp-block-coblocks-gallery-carousel-page-dot-pagination"]:
        for el in soup.select(sel): el.decompose()
    # iframe -> URL su riga propria (diventa embed in fase di render)
    for fr in soup.find_all("iframe"):
        src = html.unescape(fr.get("src", ""))
        yid = youtube_id(src)
        if yid: url = f"https://www.youtube.com/watch?v={yid}"
        elif "open.spotify.com/embed/" in src: url = src.replace("/embed/", "/").split("?")[0]
        else: url = src
        p = soup.new_tag("p"); p.string = url
        (fr.find_parent("figure") or fr).replace_with(p)
    # gallerie e caroselli -> paragrafo di sole immagini
    gal_sel = [".wp-block-kadence-advancedgallery", ".wp-block-gallery", ".blocks-gallery-grid",
               ".wp-block-coblocks-gallery-carousel", ".wp-block-coblocks-gallery-masonry",
               ".wp-block-coblocks-gallery-stacked", ".wp-block-coblocks-gallery-offset",
               ".kb-gallery-wrap-id", "[class*=kb-gallery-wrap]", ".swiper-container"]
    for sel in gal_sel:
        for g in soup.select(sel):
            if not g.parent: continue
            items = []
            for img in g.find_all("img"):
                fig = img.find_parent("figure") or img.find_parent("li")
                cap = ""
                if fig:
                    fc = fig.find(["figcaption"]) or fig.find(class_=re.compile("caption"))
                    if fc: cap = fc.get_text(" ")
                items.append(img_md(img, cap))
            # dedup (i caroselli duplicano le slide)
            seen = []; [seen.append(x) for x in items if x not in seen]
            p = soup.new_tag("p"); p["data-md"] = "\n".join(seen)
            g.replace_with(p)
    # figure singole
    for fig in soup.find_all("figure"):
        if not fig.parent: continue
        img = fig.find("img")
        if not img:
            fig.unwrap(); continue
        fc = fig.find("figcaption")
        p = soup.new_tag("p"); p["data-md"] = img_md(img, fc.get_text(" ") if fc else "")
        fig.replace_with(p)
    for img in soup.find_all("img"):
        if img.find_parent(attrs={"data-md": True}): continue
        p = soup.new_tag("span"); p["data-md"] = img_md(img)
        (img.find_parent("a") or img).replace_with(p)
    # h1 nel corpo -> h2
    for h in soup.find_all("h1"): h.name = "h2"
    # link interni relativi
    for a in soup.find_all("a", href=True):
        a["href"] = local(html.unescape(a["href"]))
    # contenitori inutili
    for el in soup.find_all(["div", "section", "span"]):
        if el.get("data-md") is None: el.unwrap()
    return soup

class Conv(MarkdownConverter):
    def convert_p(self, el, text, *args, **kw):
        if el.get("data-md") is not None:
            return "\n\n" + el["data-md"] + "\n\n"
        return super().convert_p(el, text, *args, **kw)
    def convert_span(self, el, text, *args, **kw):
        if el.get("data-md") is not None: return el["data-md"]
        return text

def to_md(h):
    soup = transform(BeautifulSoup(h, "lxml"))
    body = soup.body or soup
    md = Conv(heading_style="ATX", bullets="-", strong_em_symbol="*", escape_underscores=False,
              escape_asterisks=False).convert_soup(body)
    md = md.replace(" ", " ")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return md

def excerpt(p):
    t = BeautifulSoup(p["excerpt"]["rendered"], "lxml")
    for el in t.select(".rt-reading-time"): el.decompose()
    s = clean_text(t.get_text(" ")).replace("[…]", "").replace("[&hellip;]", "").strip()
    return (s[:230].rsplit(" ", 1)[0] + "…") if len(s) > 240 else s

def write(path, fm, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n" + body)

def title(s):
    return html.unescape(BeautifulSoup(s, "lxml").get_text()).strip()

for p in posts:
    fm = {"title": title(p["title"]["rendered"]),
          "description": excerpt(p),
          "date": p["date"][:10],
          "updated": p["modified"][:10]}
    fm["categories"] = [cat_by_id[c]["slug"] for c in p["categories"] if c in cat_by_id]
    fm["tags"] = [tag_by_id[t]["slug"] for t in p["tags"] if t in tag_by_id]
    fmid = p.get("featured_media")
    if fmid and fmid in media_by_id:
        m = media_by_id[fmid]
        fm["cover"] = local(m["source_url"])
        fm["coverAlt"] = clean_text(m.get("alt_text")) or fm["title"]
        cap = clean_text(BeautifulSoup(m["caption"]["rendered"], "lxml").get_text(" "))
        if cap: fm["coverCredit"] = cap
    fm["wpId"] = p["id"]
    write(os.path.join(ROOT, "src/content/articoli", p["slug"] + ".md"), fm, to_md(p["content"]["rendered"]))

for p in pages:
    fm = {"title": title(p["title"]["rendered"]), "updated": p["modified"][:10]}
    write(os.path.join(ROOT, "src/content/pagine", p["slug"] + ".md"), fm, to_md(p["content"]["rendered"]))

# tassonomie (nomi leggibili)
os.makedirs(os.path.join(ROOT, "src/data"), exist_ok=True)
json.dump({c["slug"]: {"name": html.unescape(c["name"]), "description": clean_text(c.get("description"))} for c in cats},
          open(os.path.join(ROOT, "src/data/categorie.json"), "w"), ensure_ascii=False, indent=1)
json.dump({t["slug"]: html.unescape(t["name"]) for t in tags},
          open(os.path.join(ROOT, "src/data/tag.json"), "w"), ensure_ascii=False, indent=1)

# immagini
ok = fail = 0
for url in sorted(needed_images):
    dest = os.path.join(ROOT, "public", urllib.parse.unquote(url[len(SITE) + 1:]))
    if os.path.exists(dest): ok += 1; continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/%"), headers={"User-Agent": "Mozilla/5.0 (migrazione lamusicadelsanto)"})
        with urllib.request.urlopen(req, timeout=25) as r, open(dest, "wb") as f: f.write(r.read())
        ok += 1
    except Exception as e:
        fail += 1; print("ERRORE immagine", url, e)
print(f"articoli {len(posts)}, pagine {len(pages)}, immagini ok {ok}, errori {fail}")
