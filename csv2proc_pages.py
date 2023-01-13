'''
Convert the CSV file to proceeding page for indexing 
'''
import os
import csv
from curses import meta

# paramters for converting
year = 2022
fn_input_csv = './content/%s/submissions.csv' % year
path_output_page = './content/proceedings/%s/' % year

# create a page
TPL_PROC_LIST = '''Title: VAHC 2022 Proceedings
Category: {year}
Date: {year}
Slug: proceedings
Authors: VAHC Committee
Summary: VAHC {year} Proceedings

# Proceedings of the {year} Workshop on Visual Analytics in Healthcare (VAHC {year})

[All VAHC Proceedings >](../all-proceedings.html)
<p>&nbsp;</p>


{content}
'''

# template for a single line in the proceedings
TPL_PROC_LINE = """
<span class="badge badge-{paper_type}">{paper_type}</span>
[{title}](../proceedings/{year}/{paper_id}.html)

*{authors}*
<p>&nbsp;</p>
"""

# template for a single indexable page
TPL_PROC_PAGE = """<!doctype html>
<html lang=en-us>
<head>
<title>VAHC {year} | {title}</title>
<meta charset="utf-8">
<meta name=viewport content="width=device-width,initial-scale=1,shrink-to-fit=no">
<meta name="citation_title" content="{title}">
{meta_authors}
<meta name="citation_publication_date" content="{publication_date}">
<meta name="citation_journal_title" content="{journal_title}">
</head>
<body>
<div class="paper">
<h2>{journal_title}</h2>
<h3>{title}</h3>
<p>{authors}</p>
<p>Abstract: {abstract}</p>
</div>
</body>
</html>
"""
TPL_PROC_PAGE_AUTHOR_LINE = '''<meta name="citation_author" content="{author}">'''


# save all records in rs
rs = []
with open(fn_input_csv, encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'* found column names: {", ".join(row)}')
            line_count += 1

        # TODO skip rows by conditions
        if row['id'] == '': continue

        # ok, save this row
        rs.append(row)
        line_count += 1

    print(f'* processed {line_count} lines.')


# make contents for proceedings and each page
lines = []
for r in rs:
    # first, make the proceeding line
    lines.append(
        TPL_PROC_LINE.format(
            title=r['title'],
            year=year,
            paper_id=r['id'],
            paper_type=r['type'],
            authors=r['authors']
        )
    )

    # second, make the indexable page
    # then we need to create many meta tags for authors
    aus = r['authors'].split(',')
    meta_authors = []
    for au in aus:
        meta_authors.append(TPL_PROC_PAGE_AUTHOR_LINE.format(
            author = au
        ))
    meta_authors = '\n'.join(meta_authors)

    # now get the page
    page = TPL_PROC_PAGE.format(
        year = year,
        title = r['title'],
        meta_authors = meta_authors,
        authors = r['authors'],
        abstract = r['abstract'],
        publication_date = r['publication_date'],
        journal_title = r['journal_title'],
    )

    # save this page as a single html
    if not os.path.exists(path_output_page): os.mkdir(path_output_page)

    fn_output_page = os.path.join(
        path_output_page,
        '%s.html' % r['id']
    )
    with open(fn_output_page, 'w', encoding='utf-8') as f:
        f.write(page)
        print('* saved the page %s' % fn_output_page)

# combine the list and line
mkd_proceedings = TPL_PROC_LIST.format(
    year = year,
    content = '\n'.join(lines)
)

# write to file!
fn_proceedings = './content/%s/proceedings.md' % year
with open(fn_proceedings, 'w', encoding='utf-8') as f:
    f.write(mkd_proceedings)
    print('* saved the proceedings list to %s' % fn_proceedings)