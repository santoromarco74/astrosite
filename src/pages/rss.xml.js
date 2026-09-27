import rss from '@astrojs/rss';
import { getArticoli, SITE } from '../lib/site';

export async function GET(context) {
  const articoli = await getArticoli();
  return rss({
    title: SITE.name,
    description: SITE.tagline,
    site: context.site,
    items: articoli.map((a) => ({ title: a.data.title, description: a.data.description, pubDate: a.data.date, link: `/${a.id}/` })),
    customData: '<language>it-it</language>',
  });
}
