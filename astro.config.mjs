// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import keystatic from '@keystatic/astro';
import rehypeSanto from './src/lib/rehype-santo.mjs';

// Keystatic (l'editor su /keystatic) gira in locale con `npm run dev`.
// Per usarlo anche online serve un adapter (Netlify/Cloudflare) + storage GitHub: vedi README.
const isDev = process.argv.includes('dev');

export default defineConfig({
  site: 'https://lamusicadelsanto.it',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [react(), sitemap(), ...(isDev ? [keystatic()] : [])],
  markdown: { rehypePlugins: [rehypeSanto] },
});
