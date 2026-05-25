VAHC Homepage
=============

The homepage of the Workshop on Visual Analytics in Healthcare (VAHC).

The site is now built with [Astro](https://astro.build/) as a static site. Yearly workshop content remains in `content/<year>/` so editors can keep working in Markdown.


Update Content
--------------

Workshop pages live under yearly folders:

```text
content/2025/
  _year.yml
  index.md
  call-for-papers.md
  program.md
  proceedings.md
  committee.md
```

Markdown pages use YAML frontmatter:

```md
---
title: Program
summary: VAHC 2025 Program
navTitle: Program
order: 30
---
```

Required:

- `title`

Optional:

- `summary`: used for metadata and the homepage subtitle.
- `navTitle`: shorter navigation label.
- `order`: yearly navigation order.
- `hidden`: hides a page from yearly navigation.

You do not need to maintain Pelican `Category`, `Slug`, or `Authors` metadata. Routes are inferred from filenames.


Install and Quick Start
-----------------------

Install dependencies with Bun:

```bash
bun install
```

Start the local dev server:

```bash
bun run dev
```

The site will be available at:

```text
http://localhost:4321/homepage/
```

Build the static site:

```bash
bun run build
```

The generated site is written to `dist/`.


Create a New Year
-----------------

Duplicate the latest year folder:

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

The homepage automatically redirects to the latest numeric year directory. There is no global `DEFAULT_YEAR` to update.


Deployment
----------

GitHub Actions builds the Astro site and deploys `dist/` to GitHub Pages. The workflow is in:

```text
.github/workflows/main.yml
```

The deployed site uses the GitHub Pages base path:

```text
https://visualanalyticshealthcare.github.io/homepage/
```


Proceedings Generation
----------------------

The repository still includes utilities to generate proceedings pages from CSV submissions:

1. `utils/csv2proc_pages.py`: converts `content/{year}/submissions.csv` into proceedings pages.
2. `utils/test_csv2proc_pages.py`: unit tests for the proceedings generator.

Usage:

```bash
cd utils
python csv2proc_pages.py 2025
python -m unittest test_csv2proc_pages.py
```

After regenerating proceedings content, run `bun run build` to verify the Astro output.
