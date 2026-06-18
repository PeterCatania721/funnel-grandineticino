#!/bin/sh
# Copia moduli, stili e risorse condivise da kesi-site (submodule o clone).
# Uso: ./scripts/sync-shared.sh [path-to-kesi-site]
set -e

KESI="${1:-shared/kesi-site}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$KESI/core" ]; then
  echo "sync-shared: kesi-site non trovato in $KESI" >&2
  exit 1
fi

copy() {
  src="$KESI/$1"
  dest="$ROOT/$2"
  if [ ! -f "$src" ]; then
    echo "sync-shared: skip (missing) $1" >&2
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
}

echo "sync-shared: da $KESI"

# Moduli condivisi
copy core/company.py core/company.py
copy core/content.py core/content.py

# CSS/JS base KESI
copy static/css/main.css static/css/main.css
copy static/js/main.js static/js/main.js

# Immagini condivise
copy static/img/favicon.png static/img/favicon.png
copy static/img/kesi-founder.jpg static/img/kesi-founder.jpg
if [ -d "$KESI/static/img/flags" ]; then
  mkdir -p "$ROOT/static/img/flags"
  cp -R "$KESI/static/img/flags/." "$ROOT/static/img/flags/"
fi

# Partial condivisi
copy templates/partials/stats.html templates/partials/stats.html
copy templates/partials/ba-pair.html templates/partials/ba-pair.html
copy templates/partials/ba-pairs.html templates/partials/ba-pairs.html

echo "sync-shared: ok"
