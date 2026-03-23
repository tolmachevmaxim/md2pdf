# md-to-pdf

This extension helps convert local Markdown files into PDF files.

The extension is installed in `~/.gemini/extensions/md-to-pdf` and bundles:

- `scripts/bootstrap.py` for one-time environment setup
- `scripts/md2pdf.py` as the wrapper entrypoint
- the `md2pdf/` Python package for the CLI logic

Preferred workflow:

1. If `~/.gemini/extensions/md-to-pdf/.venv` does not exist, run `python ~/.gemini/extensions/md-to-pdf/scripts/bootstrap.py`.
2. Convert with `python ~/.gemini/extensions/md-to-pdf/scripts/md2pdf.py <input.md> <output.pdf> --renderer cmarkgfm` on Windows/Linux.
3. Use `--renderer qlmarkdown` only on macOS with `QLMarkdown.app`.
4. Verify the output PDF exists and has non-zero size before reporting success.
