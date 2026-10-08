import os,re,sys,shutil
src,dst,P=sys.argv[1],sys.argv[2],"/"+sys.argv[3].strip("/")
shutil.rmtree(dst,ignore_errors=True); shutil.copytree(src,dst)
try: os.remove(os.path.join(dst,"_redirects"))
except FileNotFoundError: pass
esc=re.escape(P[1:])
for root,_,files in os.walk(dst):
    for f in files:
        if not f.endswith((".html",".css",".xml")): continue
        fp=os.path.join(root,f); s=open(fp,encoding="utf-8",errors="surrogateescape").read(); o=s
        if f.endswith((".html",".xml")):
            s=re.sub(r'((?:href|src|action|poster|content|data-src)=["\'])/(?!/|'+esc+'/)',r'\1'+P+'/',s)
            s=re.sub(r'(srcset=["\'])([^"\']*)',lambda m:m.group(1)+re.sub(r'(^|,\s*)/(?!/)',r'\1'+P+'/',m.group(2)),s)
            if f.endswith(".html") and '<meta name="robots"' not in s:
                s=s.replace("<head>",'<head><meta name="robots" content="noindex,nofollow">',1)
        s=re.sub(r'url\((["\']?)/(?!/|'+esc+'/)',r'url(\1'+P+'/',s)
        if s!=o: open(fp,"w",encoding="utf-8",errors="surrogateescape").write(s)
open(os.path.join(dst,".htaccess"),"w").write(f"""# Copia di prova del nuovo sito Astro (sottocartella {P}/) - non indicizzare
<IfModule mod_headers.c>
Header set X-Robots-Tag "noindex, nofollow"
</IfModule>
DirectoryIndex index.html
ErrorDocument 404 {P}/404.html
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase {P}/
RewriteRule ^feed/?$ {P}/rss.xml [R=301,L]
RewriteRule ^category/([^/]+)/?$ {P}/$1/ [R=301,L]
</IfModule>
""")
print("ok",dst)
