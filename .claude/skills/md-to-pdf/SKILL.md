---
name: md-to-pdf
description: Convert local Markdown files into PDF files. Use when asked to export, render, print, or save `.md` content as `.pdf`, especially with Playwright Chromium on Windows/Linux or QLMarkdown on macOS.
---

# md-to-pdf

Use the repository-local bootstrap and wrapper scripts.

## Quick Commands

```bash
python scripts/bootstrap.py
python scripts/md2pdf.py input.md output.pdf --renderer cmarkgfm
```

Use `--renderer qlmarkdown` only on macOS with `QLMarkdown.app`.

Details: `references/install.md` and `README.md`
