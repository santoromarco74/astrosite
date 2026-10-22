"""Genera dist/.htaccess per il sito in produzione su VHosting (LiteSpeed/Apache).

Uso: python3 scripts/htaccess.py dist

Contiene: HTTPS e dominio senza www, pagina 404, blocco totale del PHP,
risposte 410 per i vecchi indirizzi di WordPress (login, admin, xmlrpc),
redirect dalle vecchie URL (feed, categorie, immagini, slug cambiati),
intestazioni di sicurezza e cache dei file statici.
"""
import os
import sys

dist = sys.argv[1] if len(sys.argv) > 1 else "dist"
qui = os.path.dirname(os.path.abspath(__file__))

# Slug cambiati rispetto a WordPress: vecchio -> nuovo
SLUG_CAMBIATI = {
    "/paul-simon-85-anni-2/": "/paul-simon-85-anni/",
}

righe = [
    "# Generato da scripts/htaccess.py: non modificare a mano sul server,",
    "# viene sovrascritto a ogni pubblicazione.",
    "",
    "Options -Indexes",
    "DirectoryIndex index.html",
    "ErrorDocument 404 /404.html",
    "",
    "# Nessun PHP: il sito e' statico, qualsiasi .php caricato da altri non deve partire",
    '<FilesMatch "\\.(php[0-9]?|phtml|phar|cgi|pl|py|sh)$">',
    "    Require all denied",
    "</FilesMatch>",
    "",
    "<IfModule mod_rewrite.c>",
    "RewriteEngine On",
    "",
    "# Sempre HTTPS e senza www",
    "RewriteCond %{HTTPS} !=on [OR]",
    "RewriteCond %{HTTP_HOST} ^www\\. [NC]",
    "RewriteRule ^ https://lamusicadelsanto.it%{REQUEST_URI} [R=301,L,NE]",
    "",
    "# Vecchi indirizzi di WordPress: non esistono piu' (410 = eliminati per sempre)",
    "RewriteRule ^(wp-login\\.php|xmlrpc\\.php|wp-admin|wp-includes|wp-json|wp-cron\\.php)(/.*)?$ - [G,L]",
    "",
    "# Feed e categorie di WordPress",
    "RewriteRule ^feed/?$ /rss.xml [R=301,L]",
    "RewriteRule ^comments/feed/?$ /rss.xml [R=301,L]",
    "RewriteRule ^category/([^/]+)/?$ /$1/ [R=301,L]",
    "RewriteRule ^([^/]+)/feed/?$ /$1/ [R=301,L]",
    "</IfModule>",
    "",
    "<IfModule mod_alias.c>",
]
for vecchio, nuovo in SLUG_CAMBIATI.items():
    righe.append(f'Redirect 301 "{vecchio}" "{nuovo}"')

tsv = os.path.join(qui, "wp-redirects.tsv")
if os.path.exists(tsv):
    for riga in open(tsv, encoding="utf-8"):
        riga = riga.rstrip("\n")
        if not riga:
            continue
        a, b = riga.split("\t")
        righe.append(f'Redirect 301 "{a}" "{b}"')
righe += [
    "</IfModule>",
    "",
    "<IfModule mod_headers.c>",
    'Header always set Strict-Transport-Security "max-age=31536000"',
    'Header always set X-Content-Type-Options "nosniff"',
    'Header always set X-Frame-Options "SAMEORIGIN"',
    'Header always set Referrer-Policy "strict-origin-when-cross-origin"',
    'Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"',
    "</IfModule>",
    "",
    "<IfModule mod_expires.c>",
    "ExpiresActive On",
    'ExpiresByType text/html "access plus 0 seconds"',
    'ExpiresByType image/jpeg "access plus 1 month"',
    'ExpiresByType image/png "access plus 1 month"',
    'ExpiresByType image/webp "access plus 1 month"',
    'ExpiresByType image/svg+xml "access plus 1 month"',
    'ExpiresByType text/css "access plus 1 year"',
    'ExpiresByType application/javascript "access plus 1 year"',
    "</IfModule>",
    "",
]

with open(os.path.join(dist, ".htaccess"), "w", encoding="utf-8") as f:
    f.write("\n".join(righe))

# Su VHosting il file _redirects di Netlify non serve
try:
    os.remove(os.path.join(dist, "_redirects"))
except FileNotFoundError:
    pass

print(f"ok: {dist}/.htaccess ({len(righe)} righe)")
