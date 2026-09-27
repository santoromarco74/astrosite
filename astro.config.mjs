// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import keystatic from '@keystatic/astro';
import rehypeSanto from './src/lib/rehype-santo.mjs';

// Keystatic (l'editor su /keystatic) gira in locale con `npm run dev`.
// Per usarlo anche online serve un adapter (Netlify/Cloudflare) + storage GitHub: vedi README.
const k = keystatic();
const keystaticSoloDev = {
  name: 'keystatic-solo-dev',
  hooks: {
    'astro:config:setup': (opts) => { if (opts.command === 'dev') return k.hooks['astro:config:setup'](opts); },
  },
};

export default defineConfig({
  site: 'https://lamusicadelsanto.it',
  trailingSlash: 'ignore', // 'always' blocca le rotte di Keystatic; gli URL restano /slug/
  build: { format: 'directory' },
  integrations: [react(), sitemap(), keystaticSoloDev],
  markdown: { rehypePlugins: [rehypeSanto] },
});
