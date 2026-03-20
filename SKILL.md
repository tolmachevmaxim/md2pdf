---
name: md-to-pdf
description: Convert Markdown to PDF matching QLMarkdown QuickLook preview. Use when asked to export, convert, or save .md as .pdf.
allowed-tools: Bash(python3 *)
---

# MD to PDF

QLMarkdown CLI (cmark-gfm) + Playwright Chromium. GitHub-flavored styling, A4.

## Quick Commands

```bash
python3 ~/.claude/skills/md-to-pdf/scripts/md2pdf.py input.md output.pdf
```

Omit output → creates PDF next to source. Pass directory → saves there.

Full docs: README.md
