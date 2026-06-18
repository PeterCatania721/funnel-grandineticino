# funnel-grandineticino

Funnel one-page **grandineticino.ch** — repo separata da [kesi-site](https://github.com/PeterCatania721/kesi-site).

Condivide con kesi-site (via submodule / `scripts/sync-shared.sh`):

- `static/css/main.css`, `static/js/main.js`
- `core/company.py`, `core/content.py` (stats)
- immagini e partial condivisi

Il CSS e gli asset specifici del funnel restano in questo repo (`static/css/funnel.css`, template funnel, ecc.).

## Sviluppo locale

```bash
git submodule update --init --depth 1
./scripts/sync-shared.sh shared/kesi-site
cp .env.example .env
docker compose up --build
# http://localhost:8001/it/
```

Senza submodule: `./scripts/sync-shared.sh /path/to/kesi-site`

## Produzione (Hostinger VPS + Traefik)

Come `kesi-site`: `docker-compose.prod.yml` con label Traefik e `build: .`.

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Variabili obbligatorie in `.env`: `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `EMAIL_HOST_PASSWORD`.
