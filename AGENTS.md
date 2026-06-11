# AGENTS.md

Guidance for AI coding agents working in this repo.

## What this project is
A collection of **novelty desktop visual-effect apps** built with Python + tkinter, for short-video content. They have **no real functionality** — all outputs are hard-coded or random visual effects. Do not add real network calls, data collection, or anything that could make them function as actual security/identity/password tools.

## Setup / Run
```bash
pip install -r requirements.txt
python 抖音AI爆款/翻译器.py        # or any other widget under 抖音AI爆款/
```
On Windows, the `启动_*.bat` files launch each widget; `00_检测环境.bat` / `00_安装依赖.bat` handle environment checks and deps.

## Project layout
- `抖音AI爆款/` — all Python sources. Shared cyber-style UI in `_cyber_toy_ui.py`; meme popup in `_daipai_meme.py`; one file per widget.
- `启动_*.bat` — one-click launchers (each starts the matching `.py`).
- `requirements.txt` — Pillow (required), pywin32 (optional).

## Conventions
- Python 3.10+, standard library `tkinter` for GUI. Keep dependencies minimal (Pillow only, pywin32 optional).
- Widgets are intentionally non-functional. Outputs must stay fake/random/masked.
- Windows are positioned for screen recording (fixed geometry); keep that behavior.

## Don't
- Don't turn these into real tools (no real password recovery, identity lookup, etc.).
- Don't add network requests or data persistence.
