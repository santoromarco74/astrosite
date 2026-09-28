// Trasforma il Markdown del blog in HTML "da giornale":
// - paragrafo con una sola immagine  -> <figure> con didascalia (dal title dell'immagine)
// - paragrafo con più immagini       -> galleria
// - paragrafo con solo un link YouTube/Spotify -> player incorporato
// - immagini lazy e leggere (Netlify Image CDN), link esterni in nuova scheda
import { cdn, srcset } from './img.mjs';

const isWs = (n) => n.type === 'text' && !n.value.trim();
const isBr = (n) => n.type === 'element' && n.tagName === 'br';

function youtubeId(url) {
  const m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{6,})/);
  return m ? m[1] : null;
}

function alleggerisci(img, sizes = '(max-width: 760px) 100vw, 700px') {
  const src = String(img.properties.src || '');
  const set = srcset(src);
  img.properties.src = cdn(src, 1000);
  if (set) { img.properties.srcSet = set; img.properties.sizes = sizes; }
  img.properties.loading = 'lazy';
  img.properties.decoding = 'async';
}

function figureFor(img, sizes) {
  const title = img.properties.title;
  delete img.properties.title;
  const originale = String(img.properties.src || '');
  alleggerisci(img, sizes);
  // Foto cliccabile: apre la versione grande (senza JS apre l'immagine; con JS la galleria a schermo intero)
  const link = { type: 'element', tagName: 'a', properties: { className: ['zoom'], href: cdn(originale, 1800), dataDidascalia: title ? String(title) : undefined, ariaLabel: 'Ingrandisci la foto' }, children: [img] };
  const children = [link];
  if (title) children.push({ type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: String(title) }] });
  return { type: 'element', tagName: 'figure', properties: {}, children };
}

function embedFor(url) {
  const yid = youtubeId(url);
  if (yid) {
    return {
      type: 'element', tagName: 'div', properties: { className: ['embed', 'embed-video'] },
      children: [{ type: 'element', tagName: 'iframe', properties: {
        src: `https://www.youtube-nocookie.com/embed/${yid}`, title: 'Video YouTube', loading: 'lazy',
        allow: 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture', allowFullScreen: true,
      }, children: [] }],
    };
  }
  const sp = url.match(/open\.spotify\.com\/(artist|album|track|playlist)\/(\w+)/);
  if (sp) {
    return {
      type: 'element', tagName: 'div', properties: { className: ['embed', 'embed-spotify'] },
      children: [{ type: 'element', tagName: 'iframe', properties: {
        src: `https://open.spotify.com/embed/${sp[1]}/${sp[2]}`, title: 'Spotify', loading: 'lazy', height: 352,
        allow: 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture',
      }, children: [] }],
    };
  }
  return null;
}

function walk(node) {
  if (!node.children) return;
  node.children = node.children.map((child) => {
    if (child.type === 'element' && child.tagName === 'p') {
      const kids = child.children.filter((k) => !isWs(k) && !isBr(k));
      if (kids.length && kids.every((k) => k.type === 'element' && k.tagName === 'img')) {
        if (kids.length === 1) return figureFor(kids[0]);
        return { type: 'element', tagName: 'div', properties: { className: ['galleria'] }, children: kids.map((k) => figureFor(k, '(max-width: 760px) 50vw, 240px')) };
      }
      if (kids.length === 1 && kids[0].type === 'element' && kids[0].tagName === 'a') {
        const href = String(kids[0].properties.href || '');
        const txt = (kids[0].children[0] && kids[0].children[0].value) || '';
        if (txt.trim() === href) {
          const e = embedFor(href);
          if (e) return e;
        }
      }
    }
    if (child.type === 'element' && child.tagName === 'img') alleggerisci(child);
    if (child.type === 'element' && child.tagName === 'a') {
      const href = String(child.properties.href || '');
      if (/^https?:\/\//.test(href) && !href.includes('lamusicadelsanto.it')) {
        child.properties.target = '_blank';
        child.properties.rel = ['noopener'];
      }
    }
    walk(child);
    return child;
  });
}

export default function rehypeSanto() {
  return (tree) => walk(tree);
}
