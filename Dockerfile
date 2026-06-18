# Immagine Django per funnel Grandineticino.ch
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Risorse condivise da kesi-site (submodule, clone, o snapshot già in repo)
ARG KESI_SITE_REF=main
ARG GITHUB_TOKEN=
RUN set -e; \
    if [ -d shared/kesi-site/core ]; then \
      ./scripts/sync-shared.sh shared/kesi-site; \
    elif [ -n "$GITHUB_TOKEN" ]; then \
      git clone --depth 1 --branch "$KESI_SITE_REF" \
        "https://x-access-token:${GITHUB_TOKEN}@github.com/PeterCatania721/kesi-site.git" /tmp/kesi-site; \
      ./scripts/sync-shared.sh /tmp/kesi-site; \
    elif [ -f core/company.py ] && [ -f static/css/main.css ]; then \
      echo "Using vendored kesi-site assets from repo"; \
    else \
      git clone --depth 1 --branch "$KESI_SITE_REF" \
        https://github.com/PeterCatania721/kesi-site.git /tmp/kesi-site; \
      ./scripts/sync-shared.sh /tmp/kesi-site; \
    fi

RUN python manage.py compilemessages
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
