#!/usr/bin/env bash
# bootstrap.sh - set up python env and start server (for use in Git Bash or other bash on Windows)

set -euo pipefail

echo "[+] bootstrap: ensuring virtual environment exists"
if [ ! -d ".venv" ]; then
  python -m venv .venv
  echo "    created .venv"
fi

# activate the venv; Windows Git-Bash uses Scripts folder
# shellcheck disable=SC1091
source ".venv/Scripts/activate"

echo "[+] venv activated (python $(python --version))"

if [ -f requirements.txt ]; then
  echo "[+] installing/updating dependencies from requirements.txt"
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# optionally apply git pull before running (user indicated they will git pull separately)
# echo "[+] pulling latest from git"
# git pull

echo "[+] starting server...
(press Ctrl-C to stop)"
python server.py
