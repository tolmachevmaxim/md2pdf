from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

QLMARKDOWN_CLI = Path("/Applications/QLMarkdown.app/Contents/Resources/qlmarkdown_cli")

QLMARKDOWN_FLAGS = [
    "--table",
    "on",
    "--autolink",
    "on",
    "--smart-quotes",
    "on",
    "--highlight",
    "on",
    "--emoji",
    "font",
    "--footnotes",
    "on",
    "--inline-images",
    "on",
    "--math",
    "on",
    "--about",
    "off",
]

PDF_MARGINS = {
    "top": "20mm",
    "bottom": "20mm",
    "left": "15mm",
    "right": "15mm",
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    :root {{
      color-scheme: light;
      font-family: "Segoe UI", Arial, sans-serif;
    }}
    body {{
      margin: 0;
      background: #ffffff;
      color: #24292f;
    }}
    .markdown-body {{
      box-sizing: border-box;
      max-width: 900px;
      margin: 0 auto;
      padding: 32px;
      line-height: 1.6;
      font-size: 14px;
    }}
    .markdown-body h1,
    .markdown-body h2,
    .markdown-body h3,
    .markdown-body h4 {{
      line-height: 1.25;
      margin-top: 24px;
      margin-bottom: 16px;
    }}
    .markdown-body h1 {{
      padding-bottom: 10px;
      border-bottom: 1px solid #d0d7de;
    }}
    .markdown-body code,
    .markdown-body pre {{
      font-family: "Cascadia Code", "Consolas", monospace;
    }}
    .markdown-body code {{
      padding: 0.2em 0.4em;
      background: rgba(175, 184, 193, 0.2);
      border-radius: 6px;
    }}
    .markdown-body pre {{
      padding: 16px;
      overflow: auto;
      background: #f6f8fa;
      border-radius: 6px;
    }}
    .markdown-body blockquote {{
      margin: 0;
      padding: 0 1em;
      color: #57606a;
      border-left: 0.25em solid #d0d7de;
    }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
    }}
    .markdown-body th,
    .markdown-body td {{
      padding: 6px 13px;
      border: 1px solid #d0d7de;
    }}
    .markdown-body tr:nth-child(2n) {{
      background: #f6f8fa;
    }}
    .markdown-body img {{
      max-width: 100%;
    }}
  </style>
</head>
<body>
  <article class="markdown-body">
{body}
  </article>
</body>
</html>
"""


def build_file_uri(path: str | Path) -> str:
    return Path(path).resolve().as_uri()


def _strip_qlmarkdown_footer(html: str) -> str:
    html = re.sub(r"<footer[^>]*>.*?</footer>", "", html, flags=re.DOTALL)
    html = re.sub(
        r'<div[^>]*class="qlmarkdown[_-]?about[^"]*"[^>]*>.*?</div>',
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def _wrap_html(body: str) -> str:
    return HTML_TEMPLATE.format(body=body)


def _resolve_renderer(renderer: str) -> str:
    if renderer == "auto":
        return "qlmarkdown" if QLMARKDOWN_CLI.exists() else "cmarkgfm"
    return renderer


def _render_with_qlmarkdown(md_path: Path) -> str:
    if not QLMARKDOWN_CLI.exists():
        raise FileNotFoundError(
            f"QLMarkdown CLI not found at {QLMARKDOWN_CLI}. "
            "Use --renderer cmarkgfm on Windows/Linux or install QLMarkdown on macOS."
        )

    cmd = [str(QLMARKDOWN_CLI), *QLMARKDOWN_FLAGS, str(md_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"qlmarkdown_cli failed: {result.stderr.strip()}")
    return _strip_qlmarkdown_footer(result.stdout)


def _render_with_cmarkgfm(md_path: Path) -> str:
    try:
        from cmarkgfm import github_flavored_markdown_to_html
    except ImportError as exc:
        raise RuntimeError("cmarkgfm is required for --renderer cmarkgfm") from exc

    markdown = md_path.read_text(encoding="utf-8")
    html = github_flavored_markdown_to_html(markdown)
    if isinstance(html, bytes):
        html = html.decode("utf-8")
    return _wrap_html(html)


def md_to_html(md_path: str | Path, html_path: str | Path, renderer: str = "auto") -> None:
    source = Path(md_path).resolve()
    destination = Path(html_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    renderer_name = _resolve_renderer(renderer)
    if renderer_name == "qlmarkdown":
        html = _render_with_qlmarkdown(source)
    elif renderer_name == "cmarkgfm":
        html = _render_with_cmarkgfm(source)
    else:
        raise ValueError(f"Unsupported renderer: {renderer_name}")

    destination.write_text(html, encoding="utf-8")


def html_to_pdf(html_path: str | Path, pdf_path: str | Path) -> None:
    from playwright.sync_api import sync_playwright

    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(build_file_uri(html_file), wait_until="load")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_file),
            format="A4",
            margin=PDF_MARGINS,
            print_background=True,
        )
        browser.close()


def convert(md_path: str | Path, pdf_path: str | Path | None = None, renderer: str = "auto") -> str:
    source = Path(md_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    if pdf_path is None:
        target = source.with_suffix(".pdf")
    else:
        requested = Path(pdf_path)
        if requested.exists() and requested.is_dir():
            target = requested / f"{source.stem}.pdf"
        else:
            target = requested

    target = target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as handle:
        html_path = Path(handle.name)

    try:
        md_to_html(source, html_path, renderer=renderer)
        html_to_pdf(html_path, target)
    finally:
        html_path.unlink(missing_ok=True)

    return str(target)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF.")
    parser.add_argument("input", help="Path to the Markdown file.")
    parser.add_argument("output", nargs="?", help="Output PDF path.")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_option",
        help="Output PDF file or directory.",
    )
    parser.add_argument(
        "--renderer",
        choices=["auto", "cmarkgfm", "qlmarkdown"],
        default="auto",
        help="HTML renderer to use before printing the PDF.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.output and args.output_option:
        parser.error("Use either the positional output path or --output, not both.")

    output_path = args.output_option or args.output
    result = convert(args.input, output_path, renderer=args.renderer)
    size = Path(result).stat().st_size
    print(f"PDF saved: {result} ({size:,} bytes)")
    return 0
