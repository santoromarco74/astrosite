import { config, collection, fields } from '@keystatic/core';

export default config({
  // In locale salva direttamente i file. Online: { kind: 'github', repo: 'UTENTE/lamusicadelsanto' }
  storage: { kind: 'local' },
  ui: { brand: { name: 'La musica del Santo' } },
  collections: {
    articoli: collection({
      label: 'Articoli',
      slugField: 'title',
      path: 'src/content/articoli/*',
      format: { contentField: 'content' },
      entryLayout: 'content',
      columns: ['title', 'date'],
      schema: {
        title: fields.slug({ name: { label: 'Titolo' }, slug: { label: 'Indirizzo (slug)' } }),
        description: fields.text({ label: 'Sommario', multiline: true }),
        date: fields.date({ label: 'Data di pubblicazione', defaultValue: { kind: 'today' } }),
        updated: fields.date({ label: 'Ultimo aggiornamento' }),
        draft: fields.checkbox({ label: 'Bozza (non pubblicare)', defaultValue: true }),
        categories: fields.multiselect({
          label: 'Categorie',
          options: [
            { label: 'Album', value: 'album' },
            { label: 'Attualità', value: 'attualita' },
            { label: 'Film & Musical', value: 'film' },
            { label: 'Storie', value: 'storie' },
            { label: 'Biografie', value: 'biografie' },
            { label: 'Classifiche', value: 'classifiche' },
          ],
        }),
        tags: fields.array(fields.text({ label: 'Tag' }), { label: 'Tag', itemLabel: (p) => p.value }),
        cover: fields.image({ label: 'Immagine di copertina', directory: 'public/images/articoli', publicPath: '/images/articoli/' }),
        coverAlt: fields.text({ label: 'Testo alternativo copertina' }),
        coverCredit: fields.text({ label: 'Credito foto (autore, fonte, licenza)' }),
        wpId: fields.integer({ label: 'ID WordPress (storico)' }),
        content: fields.markdoc({ label: 'Testo', extension: 'md', options: { image: { directory: 'public/images/articoli', publicPath: '/images/articoli/' } } }),
      },
    }),
    pagine: collection({
      label: 'Pagine',
      slugField: 'title',
      path: 'src/content/pagine/*',
      format: { contentField: 'content' },
      schema: {
        title: fields.slug({ name: { label: 'Titolo' } }),
        updated: fields.date({ label: 'Ultimo aggiornamento' }),
        content: fields.markdoc({ label: 'Testo', extension: 'md' }),
      },
    }),
  },
});
