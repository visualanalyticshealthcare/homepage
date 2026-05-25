import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import { renderMarkdown, excerptText } from './markdown';
import { defaultPageOrder } from './years';

const rootDir = process.cwd();
const contentDir = path.join(rootDir, 'content');

export type YearData = {
  year: string;
  title: string;
  fullTitle: string;
  location?: string;
  date?: string;
  conference?: string;
  conferenceUrl?: string;
  summary?: string;
  social?: Record<string, string>;
};

export type PageData = {
  year?: string;
  slug: string;
  title: string;
  summary: string;
  summaryText: string;
  summaryHtml: string;
  navTitle: string;
  order: number;
  hidden: boolean;
  body: string;
  html: string;
  sourcePath: string;
};

function isYearDirectory(name: string) {
  return /^\d{4}$/.test(name) && fs.statSync(path.join(contentDir, name)).isDirectory();
}

function slugFromFilename(file: string) {
  return path.basename(file, '.md').replace(/_/g, '-');
}

function pageOrder(slug: string, frontmatterOrder?: unknown) {
  if (typeof frontmatterOrder === 'number') {
    return frontmatterOrder;
  }

  const index = defaultPageOrder.indexOf(slug);
  return index >= 0 ? index * 10 : 1000;
}

function readMarkdownFile(filePath: string, year?: string): PageData {
  const raw = fs.readFileSync(filePath, 'utf8');
  const parsed = matter(raw);
  const slug = slugFromFilename(filePath);
  const html = renderMarkdown(parsed.content);
  const title = String(parsed.data.title ?? parsed.data.Title ?? slug);
  const summary = String(parsed.data.summary ?? parsed.data.Summary ?? excerptText(html).slice(0, 160));
  const summaryHtml = renderMarkdown(summary).replace(/^<p>/, '').replace(/<\/p>\n?$/, '');
  const summaryText = excerptText(summaryHtml);

  return {
    year,
    slug,
    title,
    summary,
    summaryText,
    summaryHtml,
    navTitle: String(parsed.data.navTitle ?? parsed.data.navtitle ?? title),
    order: pageOrder(slug, parsed.data.order),
    hidden: Boolean(parsed.data.hidden),
    body: parsed.content,
    html,
    sourcePath: filePath
  };
}

export function getYears() {
  return fs
    .readdirSync(contentDir)
    .filter(isYearDirectory)
    .sort((a, b) => Number(a) - Number(b));
}

export function getLatestYear() {
  const years = getYears();
  return years[years.length - 1];
}

export function getYearData(year: string): YearData {
  const yearDir = path.join(contentDir, year);
  const yearFile = path.join(yearDir, '_year.yml');
  const indexPath = path.join(yearDir, 'index.md');
  const indexPage = fs.existsSync(indexPath) ? readMarkdownFile(indexPath, year) : undefined;

  if (fs.existsSync(yearFile)) {
    const loaded = yaml.load(fs.readFileSync(yearFile, 'utf8')) as Partial<YearData>;
    return {
      title: loaded.title ?? `VAHC ${year}`,
      fullTitle: loaded.fullTitle ?? loaded.title ?? `VAHC ${year}`,
      summary: loaded.summary ?? indexPage?.summary,
      ...loaded,
      year: String(loaded.year ?? year)
    };
  }

  return {
    year,
    title: `VAHC ${year}`,
    fullTitle: indexPage?.title ?? `VAHC ${year}, Workshop on Visual Analytics in Healthcare`,
    summary: indexPage?.summary ?? 'Workshop on Visual Analytics in Healthcare.',
    social: {
      linkedin: 'https://www.linkedin.com/company/visual-analytics-in-healthcare/posts/?feedView=all',
      bluesky: 'https://bsky.app/profile/vahc.bsky.social'
    }
  };
}

export function getYearPages(year: string) {
  const yearDir = path.join(contentDir, year);
  return fs
    .readdirSync(yearDir)
    .filter((file) => file.endsWith('.md'))
    .map((file) => readMarkdownFile(path.join(yearDir, file), year))
    .sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}

export function getYearPage(year: string, slug: string) {
  return getYearPages(year).find((page) => page.slug === slug);
}

export function getNavPages(year: string) {
  return getYearPages(year).filter((page) => !page.hidden);
}

export function getStandalonePages() {
  const pagesDir = path.join(contentDir, 'pages');
  if (!fs.existsSync(pagesDir)) {
    return [];
  }

  return fs
    .readdirSync(pagesDir)
    .filter((file) => file.endsWith('.md'))
    .map((file) => readMarkdownFile(path.join(pagesDir, file)))
    .sort((a, b) => a.title.localeCompare(b.title));
}

export function getStandalonePage(slug: string) {
  return getStandalonePages().find((page) => page.slug === slug);
}
