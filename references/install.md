# Install and Use

## Codex

The repository root is the skill directory. To install it from GitHub with the current Codex helper, use the repo root as the skill path:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/tolmachevmaxim/md2pdf \
  --path . \
  --name md-to-pdf
```

After installation, bootstrap the local environment once:

```bash
python scripts/bootstrap.py
python scripts/md2pdf.py input.md output.pdf --renderer cmarkgfm
```

## Claude Code

Claude Code project skills live in `.claude/skills/`. This repository includes a project skill at `.claude/skills/md-to-pdf/`, so cloning the repo already makes the skill available inside this project. For a personal install, copy or symlink the repo root to `~/.claude/skills/md-to-pdf`.

## Gemini CLI

Gemini CLI supports installable extensions from GitHub repositories. This repository includes `gemini-extension.json`, `GEMINI.md`, and `commands/md-to-pdf.toml`, so users can install it directly:

```bash
gemini extensions install https://github.com/tolmachevmaxim/md2pdf
```

The repository also includes `.gemini/commands/md-to-pdf.toml` for project-local command discovery when the repo itself is the current workspace.

## Renderers

- Windows and Linux: `--renderer cmarkgfm`
- macOS with QLMarkdown installed: `--renderer qlmarkdown`
- `auto`: prefer QLMarkdown when available, otherwise use `cmarkgfm`
