#!/usr/bin/env python3
"""
MD -> PDF converter using QLMarkdown CLI + Playwright.

Pipeline:
  1. qlmarkdown_cli converts .md -> .html (GitHub-flavored markdown, same rendering as QuickLook)
  2. Strip QLMarkdown footer ("buy me a coffee")
  3. Playwright (Chromium) prints .html -> .pdf with full CSS support

Usage:
  python3 md2pdf.py input.md                     # -> input.pdf (same directory)
  python3 md2pdf.py input.md output.pdf           # -> specified output path
  python3 md2pdf.py input.md -o ~/Downloads/      # -> ~/Downloads/input.pdf
"""

import sys
import os
import re
import subprocess
import tempfile
from pathlib import Path

QLMARKDOWN_CLI = "/Applications/QLMarkdown.app/Contents/Resources/qlmarkdown_cli"

# Default qlmarkdown_cli flags for best rendering
QLMARKDOWN_FLAGS = [
    "--table", "on",
    "--autolink", "on",
    "--smart-quotes", "on",
    "--highlight", "on",
    "--emoji", "font",
    "--footnotes", "on",
    "--inline-images", "on",
    "--math", "on",
    "--about", "off",
]

# PDF margins matching QLMarkdown visual appearance
PDF_MARGINS = {
    "top": "20mm",
    "bottom": "20mm",
    "left": "15mm",
    "right": "15mm",
}


def md_to_html(md_path: str, html_path: str) -> None:
    """Convert markdown to HTML using qlmarkdown_cli."""
    if not os.path.exists(QLMARKDOWN_CLI):
        raise FileNotFoundError(
            f"QLMarkdown CLI not found at {QLMARKDOWN_CLI}. "
            "Install QLMarkdown from https://github.com/sbarex/QLMarkdown"
        )

    # qlmarkdown_cli -o requires a directory for multiple files,
    # but for single file we use stdout redirect
    cmd = [QLMARKDOWN_CLI] + QLMARKDOWN_FLAGS + [md_path]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"qlmarkdown_cli failed: {result.stderr.decode()}")

    html = result.stdout.decode("utf-8")

    # Strip QLMarkdown footer (buy me a coffee, about section)
    html = re.sub(
        r'<footer[^>]*>.*?</footer>',
        '',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'<div[^>]*class="qlmarkdown[_-]?about[^"]*"[^>]*>.*?</div>',
        '',
        html,
        flags=re.DOTALL
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)


def html_to_pdf(html_path: str, pdf_path: str) -> None:
    """Convert HTML to PDF using Playwright Chromium."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.pdf(
            path=pdf_path,
            format="A4",
            margin=PDF_MARGINS,
            print_background=True,
        )
        browser.close()


def convert(md_path: str, pdf_path: str | None = None) -> str:
    """Convert .md file to .pdf. Returns path to generated PDF."""
    md_path = os.path.abspath(md_path)
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"File not found: {md_path}")

    if pdf_path is None:
        pdf_path = str(Path(md_path).with_suffix(".pdf"))
    elif os.path.isdir(pdf_path):
        pdf_path = os.path.join(pdf_path, Path(md_path).stem + ".pdf")

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        html_path = tmp.name

    try:
        md_to_html(md_path, html_path)
        html_to_pdf(html_path, pdf_path)
    finally:
        os.unlink(html_path)

    return pdf_path


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    md_path = sys.argv[1]
    pdf_path = None

    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        if arg == "-o" and len(sys.argv) >= 4:
            pdf_path = sys.argv[3]
        else:
            pdf_path = arg

    result = convert(md_path, pdf_path)
    print(f"PDF saved: {result} ({os.path.getsize(result):,} bytes)")


if __name__ == "__main__":
    main()
