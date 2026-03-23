# md2pdf

Convert Markdown files to PDF with Playwright Chromium.

This repository is also structured as a self-contained skill repo:

- Codex: install the repo root as the `md-to-pdf` skill
- Claude Code: project skill included at `.claude/skills/md-to-pdf/`
- Gemini CLI: installable extension via `gemini extensions install https://github.com/tolmachevmaxim/md2pdf`

The project ships:

- an installable Python package (`python -m md2pdf`)
- a wrapper script (`python scripts/md2pdf.py`)
- a bootstrap script (`python scripts/bootstrap.py`)

## Install As a Skill

### Codex

The repo root is the skill directory. The current installer equivalent is:

```powershell
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py `
  --url https://github.com/tolmachevmaxim/md2pdf `
  --path . `
  --name md-to-pdf
```

### Claude Code

Claude Code discovers project skills in `.claude/skills/`. This repository already includes `.claude/skills/md-to-pdf/SKILL.md`, so cloning the repo makes the skill available in that project.

### Gemini CLI

Gemini CLI supports installable extensions from Git repositories. This repository includes `gemini-extension.json`, `GEMINI.md`, and `commands/md-to-pdf.toml`, so this works:

```bash
gemini extensions install https://github.com/tolmachevmaxim/md2pdf
```

For repo-local use, the project also includes `.gemini/commands/md-to-pdf.toml`.

## Renderers

- `cmarkgfm`: cross-platform, works on Windows/Linux/macOS
- `qlmarkdown`: uses QLMarkdown CLI on macOS
- `auto`: uses `qlmarkdown` when available, otherwise falls back to `cmarkgfm`

## Setup

Manual setup:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m playwright install chromium
```

Or use the bundled bootstrap script:

```powershell
py scripts\bootstrap.py
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
- Codex primarily reads `SKILL.md` and `references/`; Claude Code and Gemini CLI also use the project-specific files under `.claude/` and `.gemini/`.

## Tests

```powershell
.venv\Scripts\python -m unittest discover -s tests -p "test_*.py"
```
