// Trasforma il Markdown del blog in HTML "da giornale":
// - paragrafo con una sola immagine  -> <figure> con didascalia (dal title dell'immagine)
// - paragrafo con più immagini       -> galleria
// - paragrafo con solo un link YouTube/Spotify -> player incorporato
// - immagini lazy, link esterni in nuova scheda

const isWs = (n) => n.type === 'text' && !n.value.trim();
const isBr = (n) => n.type === 'element' && n.tagName === 'br';

function youtubeId(url) {
  const m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{6,})/);
  return m ? m[1] : null;
}

function figureFor(img) {
  const title = img.properties.title;
  delete img.properties.title;
  img.properties.loading = 'lazy';
  img.properties.decoding = 'async';
  const children = [img];
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
        return { type: 'element', tagName: 'div', properties: { className: ['galleria'] }, children: kids.map(figureFor) };
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
    if (child.type === 'element' && child.tagName === 'img') {
      child.properties.loading = 'lazy';
      child.properties.decoding = 'async';
    }
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
