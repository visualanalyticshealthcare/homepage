VAHC Homepage
=============

The homepage of Workshop on Visual Analytics in Healthcare (VAHC).


Update Content
--------------

You can use the online VSCode editor to update any `.md` files and GitHub Action will automatically rebuild and publish the website after saving changes online (it will be committed to the `main` branch).


Install and Quick Start
-----------------------

The VAHC homepage is built based on [Pelican](https://getpelican.com/), a Python-powered static site generator. You can install Pelican via several different methods. The simplest is via Pip and specify using markdown:

```bash
python -m pip install "pelican[markdown]"
```

Then, you can clone the repo and go to the root folder of the cloned repo:

```bash
pelican -r -l
```

The default local dev site will be served at `http://localhost:8000/`.
You can now open web browser and check the website for development.


Deployment
----------

To deploy the generated static site on GitHub Pages, the following steps should be followed:

1. Enable workflow permissions. In "Settings / Action / General", ensure the "Workflow permissions" is set to "Read and write permissions".
2. Enable GitHub Action and add a new workflow `main.yml`. 
   Copy the following content to create the workflow action. 
   It will take a few minutes to run. Once it shows completed without any error in the Action, you can move next step.
3. Enable the GitHub Pages. In "Settings / Pages", select:
    - Source: Deploy from a branch
    - Branch: gh-pages, /(root)

If everything works fine, you can find the `gh-pages` branch has been deployed on GitHub Pages and you can access it.

```yaml
# This is a basic workflow to help you get started with Actions

name: Deploy Latest Pages by Pelican

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v3

      # Runs a single command using the runners shell
      - name: Run a one-line script
        run: echo Hello, Pelican!
          
      # Runs a build for pelican
      - name: GitHub Pages Pelican Build Action
        uses: nelsonjchen/gh-pages-pelican-action@0.1.10
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```


Settings
--------

Due to the special needs of hosting a conference website, some settings in the `pelicanconf.py` have been customized to support conference hosting workflow.

1. `DEFAULT_YEAR`. It's obvious that you need to set this variable to the conference year accordingly.
2. `PAST_EVENTS`. This will be used for generating the footer links to past events.
3. `*_SAVE_AS`. Some features are not used by a simple conference website, such as author page, tag page, archive page, category page, etc. So, they are all disabled and removed from output list.


Create New Site
---------------

The content structure of each year is very similar (or just the same) to previous year. So you can create a new website for the coming year as follows:

1. Duplicate a latest year folder in `content` and rename to target year. For example, copy the folder `2023`, paste and rename it to `2024` for the 2024.
2. Update the `Category` value in **ALL** `.md` files in the newly created folder. For example, update `Category: 2024` in the `2024\index.md`, `2024\call-for-papers.md`, etc. As this category value will be used to generate the URL and folder, please ensure you updated **ALL** category information correctly. Otherwise the generated HTML files of other year may be affected.
3. Update the contents of each article in the new folder.

Proceedings Generation
--------------------

The repository includes utilities to generate proceedings pages from CSV submissions:

1. `utils/csv2proc_pages.py`: A Python script that converts submissions CSV to proceedings pages
   - Input: `content/{year}/submissions.csv` with columns: id, type, authors, title, abstract, publication_date, citation_conference_title
   - Outputs:
     - Individual HTML pages in `content/proceedings/{year}/`
     - Proceedings markdown in `content/{year}/proceedings.md`
   - Usage:
     ```bash
     cd utils
     python csv2proc_pages.py <year>
     # Example: python csv2proc_pages.py 2024
     ```

2. `utils/test_csv2proc_pages.py`: Unit tests for the proceedings generator
   - Tests CSV parsing, proceedings markdown generation, and HTML page generation
   - Usage:
     ```bash
     cd utils
     python -m unittest test_csv2proc_pages.py
     ```

The CSV file should have the following required fields:
- `id`: Unique identifier for the submission
- `type`: Type of submission (e.g., "Poster", "Paper", "Demo")
- `authors`: Comma-separated list of authors
- `title`: Paper title
- `abstract`: Paper abstract
- `publication_date`: Publication date (YYYY-MM-DD)
- `citation_conference_title`: Full conference title
