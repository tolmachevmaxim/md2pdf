# md2pdf

Convert Markdown files to beautifully formatted PDFs that match [QLMarkdown](https://github.com/sbarex/QLMarkdown) QuickLook preview on macOS.

## How it works

Two-step pipeline:

1. **[qlmarkdown_cli](https://github.com/sbarex/QLMarkdown)** converts `.md` → `.html` using [cmark-gfm](https://github.com/github/cmark-gfm) with GitHub-flavored styling
2. **[Playwright](https://github.com/microsoft/playwright-python)** (Chromium) renders `.html` → `.pdf` with full CSS support

The result is a PDF that looks identical to macOS QuickLook preview — GitHub-style typography, syntax highlighting, tables, blockquotes, and more.

## Usage

```bash
# Creates PDF next to the .md file
python3 md2pdf.py input.md

# Specify output path
python3 md2pdf.py input.md output.pdf

# Output to directory
python3 md2pdf.py input.md -o ~/Downloads/
```

## As a Claude Code Skill

Drop into `~/.claude/skills/md-to-pdf/` and Claude Code will use it automatically when you ask to convert markdown to PDF.

```
~/.claude/skills/md-to-pdf/
├── SKILL.md          # Claude Code skill descriptor
├── README.md         # Full docs
└── scripts/
    └── md2pdf.py     # Converter script
```

## Requirements

- **macOS** with [QLMarkdown.app](https://github.com/sbarex/QLMarkdown) installed at `/Applications/QLMarkdown.app`
- **Python 3.10+**
- **Playwright** with Chromium:
  ```bash
  pip3 install playwright
  python3 -m playwright install chromium
  ```

## Features

- GitHub-flavored markdown (tables, autolinks, footnotes, math, emoji)
- Light theme with GitHub-style CSS
- Code syntax highlighting
- Blockquotes, task lists, horizontal rules
- A4 format with comfortable margins (20mm top/bottom, 15mm left/right)
- Print backgrounds (code blocks, table stripes)
- QLMarkdown promotional footer automatically stripped

## Known Issues

- `--appearance light/dark` flag in qlmarkdown_cli causes a file parsing bug — omitted by default (light theme is used automatically)

## Credits & Acknowledgements

This tool is a thin wrapper around two excellent open-source projects:

- **[QLMarkdown](https://github.com/sbarex/QLMarkdown)** by [Silvio Barbato (sbarex)](https://github.com/sbarex) — macOS QuickLook extension for Markdown files. Provides `qlmarkdown_cli` which handles the MD → HTML conversion with GitHub-flavored styling. Licensed under MIT.

- **[cmark-gfm](https://github.com/github/cmark-gfm)** by [GitHub](https://github.com/github) — GitHub's fork of the C reference implementation of CommonMark, extended with GitHub Flavored Markdown (tables, autolinks, strikethrough, task lists, etc.). The rendering engine used by QLMarkdown under the hood.

- **[Playwright for Python](https://github.com/microsoft/playwright-python)** by [Microsoft](https://github.com/microsoft) — browser automation library used for high-fidelity HTML → PDF rendering via headless Chromium. Licensed under Apache 2.0.

## License

MIT
