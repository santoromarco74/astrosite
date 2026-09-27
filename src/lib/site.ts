import { getCollection, type CollectionEntry } from 'astro:content';
import categorie from '../data/categorie.json';
import tagNames from '../data/tag.json';

export type Articolo = CollectionEntry<'articoli'>;

export const SITE = {
  name: 'La musica del Santo',
  tagline: 'Guida semiseria per autostoppisti musicali',
  motto: 'Cronache di bella musica',
  author: 'Marco Santoro',
  url: 'https://lamusicadelsanto.it',
};

// Sezioni mostrate nel menu (in ordine)
export const SEZIONI = ['album', 'storie', 'attualita', 'film'];

export async function getArticoli(): Promise<Articolo[]> {
  const all = await getCollection('articoli', ({ data }) => !data.draft);
  return all.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export function nomeCategoria(slug: string): string {
  const c = (categorie as Record<string, { name: string }>)[slug];
  return c ? c.name : slug;
}

export function nomeTag(slug: string): string {
  return (tagNames as Record<string, string>)[slug] ?? slug.replace(/-/g, ' ');
}

const GIORNI = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];
const MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];

export function dataLunga(d: Date): string {
  return `${GIORNI[d.getUTCDay()]} ${d.getUTCDate()} ${MESI[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}
export function dataBreve(d: Date): string {
  return `${d.getUTCDate()} ${MESI[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

export function minutiLettura(body: string | undefined): number {
  const words = (body ?? '').replace(/!\[[^\]]*\]\([^)\s]*(?:\s+"[^"]*")?\)/g, '').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 220));
}

export function url(a: Articolo): string {
  return `/${a.id}/`;
}

/** Primo pezzo di testo dell'articolo, senza markdown, per l'apertura in homepage. */
export function attacco(body: string | undefined, parole = 110): string {
  const testo = (body ?? '')
    .replace(/!\[[^\]]*\]\([^)\s]*(?:\s+"[^"]*")?\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .split(/\n{2,}/)
    .filter((b) => b.trim() && !/^(#|>|-|\d+\.|https?:)/.test(b.trim()))
    .join(' ')
    .replace(/[*_`]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  const w = testo.split(' ');
  return w.length > parole ? w.slice(0, parole).join(' ') + '…' : testo;
}
