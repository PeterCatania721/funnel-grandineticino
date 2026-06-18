#!/bin/sh
# Avvio del container: applica le migrazioni e lancia Gunicorn.
set -e

# Assicura che la cartella del database SQLite esista (montata come volume).
mkdir -p /app/data

python manage.py migrate --noinput
python manage.py compilemessages
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --access-logfile - \
  --error-logfile -
