// Genera le grafiche social nello stile del sito.
// Uso: NODE_PATH=$(npm root -g) node scripts/social/genera.cjs scripts/social/dati/<slug>.json
// Il JSON contiene: slug, data_evento, giorno_epoca, titolo (può contenere <br>), occhiello,
// foto (percorso relativo alla cartella del repo, es. public/images/articoli/<slug>/foto.jpg), fuoco (es. "50% 30%"),
// credito, credito_breve, testo1, testo2, interno, lancetta (facoltativo, es. "37%"),
// fascia (facoltativo: testo della fascia in alto, di default "Accadde il <data_evento>").
// Esce: public/social/<slug>-ig.jpg (1080x1350), <slug>-fb.png (1200x630) e <slug>-storia.jpg (1080x1920, storia Instagram).
// Per la storia serve anche occhiello_storia (una frase breve).
// Playwright: quello del progetto se installato, altrimenti quello globale (NODE_PATH).
const { chromium } = require('playwright');
const fs = require('node:fs'); const path = require('node:path'); const { pathToFileURL } = require('node:url');
const qui = __dirname;
const radice = path.resolve(qui, '..', '..');
const dati = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
// Fascia in alto: per gli anniversari "Accadde il <data>"; per l'attualità si può scrivere altro nel campo fascia (es. "In uscita il 30 ottobre 2026").
if (!dati.fascia) dati.fascia = `Accadde il ${dati.data_evento}`;
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/&lt;br&gt;/g, '<br>');
const riempi = (html) => html.replace(/\{\{(\w+)\}\}/g, (_, k) => k === 'foto' ? pathToFileURL(path.resolve(radice, dati.foto)).href : esc(dati[k]));
(async () => {
const browser = await chromium.launch();
for (const [nome, w, h, out, tipo] of [['ig', 1080, 1350, `${dati.slug}-ig.jpg`, 'jpeg'], ['fb', 1200, 630, `${dati.slug}-fb.png`, 'png'], ['storia', 1080, 1920, `${dati.slug}-storia.jpg`, 'jpeg']]) {
  const tmp = path.join(qui, `.tmp-${nome}.html`);
  fs.writeFileSync(tmp, riempi(fs.readFileSync(path.join(qui, `${nome}.html`), 'utf8')).replace('<div class="tela">', `<div class="tela" style="--lancetta:${dati.lancetta || '37%'}">`));
  const p = await browser.newPage({ viewport: { width: w, height: h } });
  await p.goto(pathToFileURL(tmp).href); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const fuori = await p.evaluate(() => { const t = document.querySelector('.tela'); return t.scrollHeight > t.clientHeight + 1; });
  if (fuori) console.warn(`ATTENZIONE: il contenuto di ${nome} esce dalla tela, accorcia i testi`);
  await p.screenshot({ path: path.join(radice, 'public', 'social', out), type: tipo, ...(tipo === 'jpeg' ? { quality: 90 } : {}) });
  await p.close(); fs.unlinkSync(tmp);
  console.log('ok', out);
}
await browser.close();
})();
