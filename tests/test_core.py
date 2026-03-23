from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from md2pdf.core import build_file_uri, convert, html_to_pdf, main, md_to_html


class Md2PdfTests(unittest.TestCase):
    def test_build_file_uri_escapes_spaces(self) -> None:
        with tempfile.TemporaryDirectory(prefix="md2pdf uri ") as tmpdir:
            html_path = Path(tmpdir) / "sample file.html"
            uri = build_file_uri(html_path)

        self.assertTrue(uri.startswith("file:"))
        self.assertIn("sample%20file.html", uri)

    def test_md_to_html_cmarkgfm_writes_html_document(self) -> None:
        fixture = Path("tests/fixtures/sample.md").resolve()
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "sample.html"
            md_to_html(fixture, html_path, renderer="cmarkgfm")
            html = html_path.read_text(encoding="utf-8")

        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn('<article class="markdown-body">', html)
        self.assertIn("<table>", html)

    def test_html_to_pdf_uses_as_uri_and_creates_output_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "input file.html"
            html_path.write_text("<html><body>ok</body></html>", encoding="utf-8")
            pdf_path = Path(tmpdir) / "nested" / "output.pdf"

            page = MagicMock()
            browser = MagicMock()
            browser.new_page.return_value = page
            chromium = MagicMock()
            chromium.launch.return_value = browser
            playwright = MagicMock()
            playwright.chromium = chromium
            context = MagicMock()
            context.__enter__.return_value = playwright
            context.__exit__.return_value = False

            with patch("playwright.sync_api.sync_playwright", return_value=context):
                html_to_pdf(html_path, pdf_path)

            self.assertTrue(pdf_path.parent.exists())
            page.goto.assert_called_once_with(build_file_uri(html_path), wait_until="load")
            page.pdf.assert_called_once()
            self.assertEqual(page.pdf.call_args.kwargs["path"], str(pdf_path.resolve()))

    def test_main_passes_renderer_and_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / "result.pdf"
            pdf_path.write_bytes(b"pdf")

            with patch("md2pdf.core.convert", return_value=str(pdf_path)) as convert_mock:
                exit_code = main(
                    ["tests/fixtures/sample.md", str(pdf_path), "--renderer", "cmarkgfm"]
                )

        self.assertEqual(exit_code, 0)
        convert_mock.assert_called_once_with(
            "tests/fixtures/sample.md", str(pdf_path), renderer="cmarkgfm"
        )

    def test_convert_rejects_missing_input(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert("tests/fixtures/missing.md", renderer="cmarkgfm")


if __name__ == "__main__":
    unittest.main()
