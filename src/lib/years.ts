export const defaultPageOrder = [
  'index',
  'call-for-papers',
  'docconsortium',
  'program',
  'panel',
  'keynote',
  'workshop-event',
  'proceedings',
  'committee'
];

export const pastEvents = [
  [2024, 'San Francisco, CA'],
  [2023, 'Melbourne, Australia'],
  [2022, 'Washington, D.C.'],
  [2021, 'Virtual'],
  [2020, 'Virtual'],
  [2019, 'Vancouver, BC, Canada'],
  [2018, 'San Francisco, CA'],
  [2017, 'Phoenix, AZ'],
  [2016, 'Chicago, IL'],
  [2015, 'Chicago, IL'],
  [2014, 'Washington, D.C.'],
  [2013, 'Washington, D.C.'],
  [2012, 'Seattle, WA'],
  [2011, 'Providence, RI'],
  [2010, 'Salt Lake City, GA']
] as const;

export function sitePath(path = '') {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const cleanPath = path.replace(/^\//, '');
  return cleanPath ? `${base}/${cleanPath}` : `${base}/`;
}

export function pageHref(year: string, slug = 'index') {
  if (slug === 'index') {
    return sitePath(`${year}/`);
  }

  return sitePath(`${year}/${slug}.html`);
}

export function staticHref(path: string) {
  return sitePath(path);
}
