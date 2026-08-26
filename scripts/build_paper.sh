#!/bin/bash
# Render the manuscript and sync it under the site's /paper/web/ route.
# The public /paper/ URL serves the hand-written wrapper (site/paper/index.html),
# never the raw render — see the paper-embed pattern. Bump the ?v= version in
# the wrapper on every revision; tests/test_paper_embed.py locks the lockstep.
set -euo pipefail
cd "$(dirname "$0")/.."

QUARTO_PYTHON="$PWD/.venv/bin/python" quarto render paper/index.qmd

mkdir -p site/paper/web
rsync -a --delete paper/out/index.html paper/out/index.pdf site/paper/web/
rsync -a --delete paper/out/index_files/ site/paper/web/index_files/
echo "synced paper/out -> site/paper/web"
