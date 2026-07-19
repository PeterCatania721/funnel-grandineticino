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

Path VPS: `/docker/funnel-grandineticino`.

```bash
# sul VPS (dopo aver installato .env.identity con machine identity Infisical)
./scripts/deploy-grandineticino.sh
```

File sul server (non in git i secret):

| File | Contenuto |
|------|-----------|
| `config.env` | non-secret (host, `info@kesi.biz`, path Infisical `/`) |
| `.env` | `SECRET_KEY` (+ cache password solo se serve fallback) |
| `.env.identity` | `INFISICAL_PROJECT_ID`, `INFISICAL_MACHINE_CLIENT_ID`, `INFISICAL_MACHINE_CLIENT_SECRET` |

**Email (regola fissa, non cambiare a meno di richiesta esplicita):**

- mittente / SMTP user / destinatari lead = sempre `info@kesi.biz`
- password = **sempre** da Infisical `KESI_FUNNEL_GRANDINETICINO_EMAIL_PASSWORD`
- a ogni **deploy** lo script riallinea la password
- a ogni **avvio container** `infisical-entrypoint.sh` re-inieetta i secret da Infisical (path `/`)


## Componenti UI

I partial del funnel (form, header, sezioni, …) sono anche esposti come:

```django
{% include "components/funnel-form-card.html" %}
```

Catalogo: [`docs/COMPONENTS.md`](docs/COMPONENTS.md). Elenco: `./scripts/list-components.sh`.
