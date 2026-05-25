import { marked } from 'marked';

marked.setOptions({
  gfm: true,
  breaks: false
});

export function renderMarkdown(markdown: string) {
  return marked.parse(markdown) as string;
}

export function excerptText(html: string) {
  return html
    .replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function splitImportantDates(html: string) {
  const headingPattern = /<h1[^>]*>\s*IMPORTANT DATES\s*<\/h1>/i;
  const match = html.match(headingPattern);

  if (!match || match.index === undefined) {
    return { mainHtml: html, datesHtml: '' };
  }

  const start = match.index;
  const afterHeading = start + match[0].length;
  const nextHeading = html.slice(afterHeading).search(/<h1[^>]*>/i);
  const end = nextHeading >= 0 ? afterHeading + nextHeading : html.length;

  return {
    mainHtml: `${html.slice(0, start)}${html.slice(end)}`.trim(),
    datesHtml: html.slice(start, end).trim()
  };
}
