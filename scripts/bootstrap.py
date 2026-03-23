#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap the md-to-pdf skill environment.")
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable used to create the virtual environment.",
    )
    parser.add_argument(
        "--venv",
        default=".venv",
        help="Virtual environment directory, relative to the skill root.",
    )
    parser.add_argument(
        "--skip-playwright",
        action="store_true",
        help="Skip 'python -m playwright install chromium'.",
    )
    args = parser.parse_args(argv)

    skill_root = Path(__file__).resolve().parents[1]
    venv_dir = (skill_root / args.venv).resolve()
    if not venv_dir.exists():
        run([args.python, "-m", "venv", str(venv_dir)])

    python_exe = venv_python(venv_dir)
    run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(python_exe), "-m", "pip", "install", "-e", str(skill_root)])
    if not args.skip_playwright:
        run([str(python_exe), "-m", "playwright", "install", "chromium"])

    print(f"Bootstrap complete: {python_exe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
