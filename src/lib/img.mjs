// Immagini leggere: su Netlify passano dall'Image CDN (WebP ridimensionate al volo).
// In locale (npm run dev / build fuori da Netlify) restano gli originali.
const suNetlify = process.env.NETLIFY === 'true' || process.env.IMG_CDN === '1';
const LARGHEZZE = [400, 700, 1000, 1400];

function locale(src) {
  return typeof src === 'string' && (src.startsWith('/wp-content/') || src.startsWith('/images/'));
}

export function cdn(src, w) {
  if (!suNetlify || !locale(src)) return src;
  return `/.netlify/images?url=${encodeURIComponent(src)}&w=${w}&fm=webp&q=72`;
}

export function srcset(src, max = 1400) {
  if (!suNetlify || !locale(src)) return undefined;
  return LARGHEZZE.filter((w) => w <= max).map((w) => `${cdn(src, w)} ${w}w`).join(', ');
}
