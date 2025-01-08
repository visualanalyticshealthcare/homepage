import unittest
import os
import csv
from csv2proc_pages import (
    TPL_PROC_LIST,
    TPL_PROC_LINE,
    TPL_PROC_PAGE,
    TPL_PROC_PAGE_AUTHOR_LINE,
)


class TestProceedings(unittest.TestCase):
    def setUp(self):
        # Test data based on actual submissions
        self.test_data = {
            "input_csv": "test_submissions.csv",
            "output_dir": "test_proceedings",
            "year": 2024,
            "sample_record": {
                "id": "1",
                "type": "Poster",
                "authors": "Advika Sumit, Gargi Rajput, Andy Gao, Scott Vennemeyer and Danny T.Y. Wu",
                "title": "Developing a Data Dashboard to Support Student Success in a Medical Sciences Baccalaureate Program",
                "abstract": "Pre-medical students face the challenge of managing rigorous academic and extracurricular demands...",
                "publication_date": "2024-11-09",
                "citation_conference_title": "The 15th Workshop on Visual Analytics in Healthcare (VAHC 2024)",
            },
        }

        # Create test CSV
        with open(self.test_data["input_csv"], "w", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "type",
                    "authors",
                    "title",
                    "abstract",
                    "publication_date",
                    "citation_conference_title",
                ],
            )
            writer.writeheader()
            writer.writerow(self.test_data["sample_record"])

        # Create test output directory
        os.makedirs(self.test_data["output_dir"], exist_ok=True)

    def test_csv_parsing(self):
        """Test that CSV is correctly parsed"""
        records = []
        with open(self.test_data["input_csv"], encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row.get("id") and row.get("title"):
                    records.append(row)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], self.test_data["sample_record"]["id"])
        self.assertEqual(records[0]["title"], self.test_data["sample_record"]["title"])

    def test_proceedings_generation(self):
        """Test that proceedings markdown is correctly generated"""
        # Generate proceedings line
        proc_line = TPL_PROC_LINE.format(
            title=self.test_data["sample_record"]["title"],
            year=self.test_data["year"],
            paper_id=self.test_data["sample_record"]["id"],
            paper_type=self.test_data["sample_record"]["type"].lower(),
            authors=self.test_data["sample_record"]["authors"],
        )

        # Verify proceedings line contains expected elements
        self.assertIn(self.test_data["sample_record"]["title"], proc_line)
        self.assertIn(self.test_data["sample_record"]["authors"], proc_line)
        self.assertIn(
            f"badge-{self.test_data['sample_record']['type'].lower()}", proc_line
        )

    def test_html_generation(self):
        """Test that individual HTML files are correctly generated"""
        # Generate author meta tags
        authors = self.test_data["sample_record"]["authors"].split(",")
        meta_authors = []
        for author in authors:
            meta_authors.append(TPL_PROC_PAGE_AUTHOR_LINE.format(author=author.strip()))
        meta_authors = "\n".join(meta_authors)

        # Generate HTML page
        page = TPL_PROC_PAGE.format(
            year=self.test_data["year"],
            title=self.test_data["sample_record"]["title"],
            meta_authors=meta_authors,
            authors=self.test_data["sample_record"]["authors"],
            abstract=self.test_data["sample_record"]["abstract"],
            publication_date=self.test_data["sample_record"]["publication_date"],
            citation_conference_title=self.test_data["sample_record"][
                "citation_conference_title"
            ],
            pdf_url=f"./{self.test_data['sample_record']['id']}.pdf",
        )

        # Verify HTML contains expected elements
        self.assertIn(self.test_data["sample_record"]["title"], page)
        self.assertIn(self.test_data["sample_record"]["authors"], page)
        self.assertIn(self.test_data["sample_record"]["abstract"], page)
        self.assertIn(
            self.test_data["sample_record"]["citation_conference_title"], page
        )

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_data["input_csv"]):
            os.remove(self.test_data["input_csv"])
        if os.path.exists(self.test_data["output_dir"]):
            os.rmdir(self.test_data["output_dir"])


if __name__ == "__main__":
    unittest.main()
