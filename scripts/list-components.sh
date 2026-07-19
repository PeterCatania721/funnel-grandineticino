#!/usr/bin/env bash
# Elenca i componenti UI disponibili in questo repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "== components/ (alias stabili) =="
ls -1 "$ROOT/templates/components" 2>/dev/null | sed 's/\.html$//' | sort || true
echo ""
echo "== partials/ =="
find "$ROOT/templates/partials" -name '*.html' | sed "s|$ROOT/templates/||" | sort
echo ""
echo "Vedi docs/COMPONENTS.md per API e sync."
