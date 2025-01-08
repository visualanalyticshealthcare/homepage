"""
Convert the CSV file to proceeding page for indexing 
"""

import os
import csv
from typing import List, Dict
import argparse


class ProceedingsGenerator:
    def __init__(self, year: int):
        self.year = year
        self.fn_input_csv = f"../content/{year}/submissions.csv"
        self.path_output_page = f"../content/proceedings/{year}/"

    def read_csv(self) -> List[Dict]:
        """Read and parse the CSV file"""
        records = []
        try:
            with open(self.fn_input_csv, encoding="utf-8-sig") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                print(f'* found column names: {", ".join(csv_reader.fieldnames)}')

                for row in csv_reader:
                    # Skip empty rows
                    if not any(row.values()):
                        continue

                    # Skip rows without required fields
                    if (
                        not row.get("id")
                        or not row.get("title")
                        or not row.get("authors")
                    ):
                        continue

                    # Clean whitespace
                    cleaned_row = {k: v.strip() if v else v for k, v in row.items()}
                    records.append(cleaned_row)

            print(f"* processed {len(records)} records")
            return records
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
            return []

    def generate_html_page(self, record: Dict) -> str:
        """Generate individual HTML page for a record"""
        # Generate author meta tags
        authors = record["authors"].split(",")
        meta_authors = []
        for author in authors:
            meta_authors.append(TPL_PROC_PAGE_AUTHOR_LINE.format(author=author.strip()))
        meta_authors = "\n".join(meta_authors)

        # Generate HTML
        return TPL_PROC_PAGE.format(
            year=self.year,
            title=record["title"],
            meta_authors=meta_authors,
            authors=record["authors"],
            abstract=record["abstract"],
            publication_date=record["publication_date"],
            citation_conference_title=record["citation_conference_title"],
            pdf_url=f"./{record['id']}.pdf",
        )

    def generate_proceedings_line(self, record: Dict) -> str:
        """Generate a proceedings line for a record"""
        return TPL_PROC_LINE.format(
            title=record["title"],
            year=self.year,
            paper_id=record["id"],
            paper_type=record["type"].lower(),
            authors=record["authors"],
        )

    def generate_proceedings(self, records: List[Dict]) -> str:
        """Generate the full proceedings markdown"""
        lines = [self.generate_proceedings_line(r) for r in records]
        return TPL_PROC_LIST.format(year=self.year, content="\n".join(lines))

    def save_html_pages(self, records: List[Dict]) -> None:
        """Save individual HTML pages"""
        if not os.path.exists(self.path_output_page):
            os.makedirs(self.path_output_page)

        for record in records:
            html_content = self.generate_html_page(record)
            output_path = os.path.join(self.path_output_page, f"{record['id']}.html")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                print(f"* saved page {output_path}")

    def save_proceedings(self, content: str) -> None:
        """Save the proceedings markdown file"""
        output_path = f"../content/{self.year}/proceedings.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"* saved proceedings to {output_path}")

    def run(self) -> None:
        """Run the full proceedings generation process"""
        records = self.read_csv()
        if not records:
            print("No valid records found. Exiting.")
            return

        proceedings_content = self.generate_proceedings(records)
        self.save_proceedings(proceedings_content)
        self.save_html_pages(records)


# Templates (unchanged)
TPL_PROC_LIST = """Title: VAHC {year} Proceedings
Category: {year}
Date: {year}
Slug: proceedings
Authors: VAHC Committee
Summary: VAHC {year} Proceedings


# All Proceedings

[All VAHC Proceedings >](../page/all-proceedings.html)
<p>&nbsp;</p>


# Proceedings of the {year} Workshop on Visual Analytics in Healthcare (VAHC {year})

{content}
"""

TPL_PROC_LINE = """
<span class="badge badge-{paper_type}">{paper_type}</span>
[{title}](../proceedings/{year}/{paper_id}.html)

*{authors}*

[Full-text PDF](../proceedings/{year}/{paper_id}.pdf)
<p>&nbsp;</p>
"""

TPL_PROC_PAGE = """<!doctype html>
<html lang=en-us>
<head>
<title>VAHC {year} | {title}</title>
<meta charset="utf-8">
<meta name=viewport content="width=device-width,initial-scale=1,shrink-to-fit=no">
<meta name="citation_title" content="{title}">
{meta_authors}
<meta name="citation_publication_date" content="{publication_date}">
<meta name="citation_conference_title" content="{citation_conference_title}">
<meta name="citation_pdf_url" content="{pdf_url}">
</head>
<body>
<div class="paper">
<h2>{citation_conference_title}</h2>
<h3>{title}</h3>
<p>{authors}</p>
<p>Abstract: {abstract}</p>
<p>
<a href="{pdf_url}">Full-text PDF</a>
</p>
</div>
</body>
</html>
"""

TPL_PROC_PAGE_AUTHOR_LINE = """<meta name="citation_author" content="{author}">"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate proceedings pages from CSV submissions."
    )
    parser.add_argument("year", type=int, help="Conference year (e.g., 2024)")
    args = parser.parse_args()

    generator = ProceedingsGenerator(args.year)
    generator.run()
