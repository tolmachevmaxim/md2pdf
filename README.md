# md2pdf

Convert Markdown files to PDF with Playwright Chromium.

The project now ships both:

- an installable Python package (`python -m md2pdf`)
- a wrapper script (`python scripts/md2pdf.py`)

## Renderers

- `cmarkgfm`: cross-platform, works on Windows/Linux/macOS
- `qlmarkdown`: uses QLMarkdown CLI on macOS
- `auto`: uses `qlmarkdown` when available, otherwise falls back to `cmarkgfm`

## Windows quick start

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m playwright install chromium
```

## Usage

```powershell
.venv\Scripts\python -m md2pdf tests/fixtures/sample.md output/sample.pdf --renderer cmarkgfm
.venv\Scripts\python scripts/md2pdf.py tests/fixtures/sample.md output/sample-wrapper.pdf --renderer cmarkgfm
```

If the output parent directory does not exist, `md2pdf` creates it automatically.

## Notes

- Windows and Linux should use `--renderer cmarkgfm`.
- macOS users can use `--renderer qlmarkdown` if `QLMarkdown.app` is installed.
- Playwright requires a one-time browser install via `python -m playwright install chromium`.

## Tests

```powershell
.venv\Scripts\python -m unittest discover -s tests -p "test_*.py"
```
