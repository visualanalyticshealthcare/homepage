# Astro Migration Plan

## Goal

Replace the current Pelican build with a simpler Astro-based static site while keeping the existing yearly content workflow:

- Keep all workshop content in `content/<year>/`.
- Keep one GitHub repository for all years.
- Deploy static files to GitHub Pages.
- Avoid any backend or CMS.
- Let editors focus on Markdown content instead of route metadata such as `Category` and `Slug`.

The target workflow for a new year should be:

```bash
cp -R content/2025 content/2026
```

Then update only the shared year data and page content.

Once the migration is finished, the GitHub action should also be changed. Additionally, when we access the homepage, it will automatically choose the latest one, just as the current behavior.

## Current Repo Shape

The current site is built with Pelican.

Important existing paths:

```text
content/
  2022/
  2023/
  2024/
  2025/
    index.md
    call-for-papers.md
    committee.md
    docconsortium.md
    proceedings.md
    program.md
    workshop-event.md
  files/
  images/
  pages/
  proceedings/

themes/vahc-theme/
output/
pelicanconf.py
publishconf.py
myplugins.py
```

Current Markdown files use Pelican metadata:

```text
Title: Program
Category: 2025
Date: 2025-03-11
Slug: program
Authors: VAHC Committee
Summary: VAHC 2025 Program
```

The migration should remove the need to maintain `Category` and `Slug` manually.

## Recommended Target Structure

Add Astro files while preserving the current `content/<year>/` organization.

```text
content/
  2025/
    _year.yml
    index.md
    call-for-papers.md
    committee.md
    docconsortium.md
    proceedings.md
    program.md
    workshop-event.md
  2026/
    _year.yml
    index.md
    call-for-papers.md
    committee.md
    proceedings.md
    program.md
  images/
  files/

src/
  layouts/
    WorkshopLayout.astro
    YearHomeLayout.astro
  pages/
    index.astro
    [year]/
      index.astro
      [slug].astro
  components/
    SiteHeader.astro
    SiteFooter.astro
    YearNav.astro
    ImportantDates.astro
  lib/
    content.ts
    markdown.ts
    years.ts
  styles/
    global.css

astro.config.mjs
package.json
bun.lock
```

## Content Conventions

### Year Data

Each year should have a single shared data file:

```text
content/2026/_year.yml
```

Example:

```yaml
year: 2026
title: VAHC 2026
fullTitle: VAHC 2026, Workshop on Visual Analytics in Healthcare
location: TBD
date: TBD
conference: IEEE VIS 2026
conferenceUrl: https://ieeevis.org/
summary: Workshop on Visual Analytics in Healthcare.
social:
  linkedin: https://www.linkedin.com/company/visual-analytics-in-healthcare/posts/?feedView=all
  bluesky: https://bsky.app/profile/vahc.bsky.social
```

This file replaces global settings such as `DEFAULT_YEAR` for year-specific content.

### Page Markdown

Prefer YAML frontmatter:

```md
---
title: Program
summary: VAHC 2026 Program
navTitle: Program
order: 30
---

This is the VAHC 2026 program.
```

Required fields:

- `title`

Optional fields:

- `summary`: used for SEO description and page subtitle.
- `navTitle`: shorter label for navigation.
- `order`: controls navigation order.
- `hidden`: hides a page from yearly navigation.

Do not require:

- `Category`
- `Slug`
- `Authors`

The route should be inferred from file path:

```text
content/2026/index.md           -> /2026/
content/2026/program.md         -> /2026/program/
content/2026/committee.md       -> /2026/committee/
content/2026/call-for-papers.md -> /2026/call-for-papers/
```

## Migration Strategy

### Phase 1: Add Astro Without Removing Pelican

Add Astro alongside the existing Pelican setup.

Tasks:

1. Add `package.json`, `astro.config.mjs`, and `src/`.
2. Keep Pelican files untouched during the first pass.
3. Build Astro output into `dist/`.
4. Verify generated routes locally.

This keeps the existing site deployable while the migration is tested.

### Phase 2: Implement Content Loader

Create helper code under `src/lib/` that:

1. Lists valid year directories under `content/`.
2. Detects the latest year automatically by max numeric directory name.
3. Reads `content/<year>/_year.yml`.
4. Reads Markdown pages in `content/<year>/`.
5. Derives route slugs from filenames.
6. Sorts navigation by `order`, then by a default page order.

Default nav order:

```text
index
call-for-papers
docconsortium
program
workshop-event
proceedings
committee
```

If a file does not exist for a given year, it should simply not appear in that year's navigation.

### Phase 3: Convert Metadata

Convert existing Pelican metadata to YAML frontmatter.

Before:

```md
Title: Program
Category: 2025
Date: 2025-03-11
Slug: program
Authors: VAHC Committee
Summary: VAHC 2025 Program

This is the VAHC 2025 program.
```

After:

```md
---
title: Program
summary: VAHC 2025 Program
---

This is the VAHC 2025 program.
```

Rules:

- `Title` -> `title`
- `Summary` -> `summary`
- Drop `Category`
- Drop `Slug`
- Drop `Authors` unless it is still useful
- Keep `Date` only if needed for news sorting or page metadata

This can be done incrementally year by year.

### Phase 4: Recreate Current Theme

Port the current visual design from `themes/vahc-theme/` into Astro:

- `base.html` -> `WorkshopLayout.astro`
- `article.html` -> page rendering logic in `WorkshopLayout.astro`
- `index.html` redirect -> `src/pages/index.astro`
- `style.css` -> `src/styles/global.css`
- static theme images -> `public/theme/img/` or imported assets

Keep the site visually close to the current VAHC site at first. Redesign can happen later.

### Phase 5: Preserve Existing URLs

Decide whether to keep `.html` URLs.

Current Pelican URLs:

```text
/2025/program.html
/2025/committee.html
```

Preferred Astro URLs:

```text
/2025/program/
/2025/committee/
```

If old links must continue to work, add redirect pages or configure Astro output to preserve file-style URLs where practical.

For GitHub Pages, also set the correct base path:

```js
// astro.config.mjs
import { defineConfig } from 'astro/config'

export default defineConfig({
  site: 'https://visualanalyticshealthcare.github.io',
  base: '/homepage',
  output: 'static'
})
```

### Phase 6: Update GitHub Pages Workflow

Replace the Pelican GitHub Action with an Astro build and Pages deploy workflow.

Use `bun` for local JavaScript work if following the local workspace convention.

Workflow outline:

```yaml
name: Deploy Astro Site

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

## New Year Workflow After Migration

For VAHC 2026:

```bash
cp -R content/2025 content/2026
```

Then edit:

```text
content/2026/_year.yml
content/2026/index.md
content/2026/call-for-papers.md
content/2026/program.md
content/2026/committee.md
```

No need to edit:

- `Category`
- `Slug`
- global `DEFAULT_YEAR`
- navigation config

The homepage should automatically redirect to the latest numeric year directory.

## Open Decisions

1. Keep current `.html` URLs exactly, or move to slash URLs?
2. Keep Bootstrap 4 for the first Astro version, or replace it with custom CSS?
3. Convert all historical years immediately, or only convert the latest year first?
4. Keep generated `output/` in the repo, or remove it after Astro deployment is stable?
5. Keep proceedings generation as Python scripts, or migrate proceedings generation into Astro later?

## Recommendation

Use Astro for the migration, not VitePress.

Reason:

- The current repo is a multi-year content website, not a documentation site.
- Astro can preserve `content/<year>/` cleanly.
- Routes can be inferred from folders and filenames.
- Markdown remains the main editing format.
- GitHub Pages deployment stays static.
- The final site can be SEO-friendly, responsive, and mostly static HTML.

VitePress is still a good fit for tutorial notes or documentation pages, but it is not the best fit for this VAHC homepage migration.
