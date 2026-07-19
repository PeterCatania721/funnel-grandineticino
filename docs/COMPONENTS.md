# Componenti UI KESI (kesi-site + funnel-grandineticino)

Catalogo dei partial/componenti riusabili. Usarli con:

```django
{% include "components/<nome>.html" %}
{# oppure direttamente #}
{% include "partials/<nome>.html" with ... %}
```

I file in `templates/components/` sono alias stabili verso `templates/partials/`.
Passare variabili con `with` (es. `form=form`) — il contesto viene ereditato dall’include interno.

## Catalogo kesi-site (sito KESI 2026)

| Componente | Path include | Note |
|------------|--------------|------|
| **funnel-form** | `components/funnel-form.html` | Card wizard hero (wrap `#funnel-form`) |
| **funnel-form-card** | `components/funnel-form-card.html` | Card prominent + wizard (param: `form`, `wrap_id`, `heading_level`, …) |
| **funnel-form-wizard** | `components/funnel-form-wizard.html` | Solo form multi-step Alpine |
| **funnel-form-head** | `components/funnel-form-head.html` | Logo + titolo “Preventivo gratuito” |
| **funnel-form-bottom** | `components/funnel-form-bottom.html` | Seconda istanza form (bottom page) |
| header | `components/header.html` | Nav principale |
| footer | `components/footer.html` | Footer |
| cta | `components/cta.html` | Blocco call-to-action |
| stats | `components/stats.html` | Statistiche |
| advantages | `components/advantages.html` | Vantaggi |
| advantage-icon | `components/advantage-icon.html` | Icona vantaggio |
| page-hero | `components/page-hero.html` | Hero di pagina |

### Asset form preventivo

| Asset | Path |
|-------|------|
| CSS | `static/css/funnel-form.css` |
| JS wizard | `static/js/funnel.js` |
| JS telefono | `static/js/tel-prefix.js` |
| Form Django | `core/preventivo_form.py` (`PreventivoForm`) |
| Validazione tel | `core/phone.py` |

Pagina che lo usa: `templates/pages/preventivo.html` → `{% include "components/funnel-form-card.html" ... %}`.

## Catalogo funnel-grandineticino (extra)

Oltre ai form, il funnel espone:

| Componente | Path |
|------------|------|
| funnel-header | `partials/funnel-header.html` |
| funnel-footer | `partials/funnel-footer.html` |
| ba-pair / ba-pairs | `partials/ba-pair.html`, `ba-pairs.html` |
| comparison-table, faq, mission, mistakes, urgency | `partials/funnel/*` |

## Sync tra repo

```bash
# Da kesi-site verso funnel (asset “classici”)
cd funnel-grandineticino && ./scripts/sync-shared.sh /path/to/kesi-site

# Copia componente form funnel → kesi (se aggiorni il form nel funnel)
cd kesi-site && ./scripts/sync-funnel-form-from-funnel.sh /path/to/funnel-grandineticino

# Elenco componenti
./scripts/list-components.sh
```

Regola: **il modulo preventivo multi-step è unico** (stesso markup/CSS/JS). Su kesi invia email; sul funnel salva anche lead SQLite.
