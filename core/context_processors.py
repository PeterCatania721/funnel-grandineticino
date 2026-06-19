from core.company import COMPANY
from core.content import ADVANTAGES, REFERENCES, SERVICES, STATS, TARGETS, TECHNOLOGIES, TIMELINE


def company(request):
    """Espone i dati aziendali a tutti i template come `company`."""
    return {"company": COMPANY}


def site_content(request):
    """Espone i contenuti centralizzati (servizi, vantaggi, target, stat)."""
    return {
        "services": SERVICES,
        "advantages": ADVANTAGES,
        "targets": TARGETS,
        "stats": STATS,
        "timeline": TIMELINE,
        "references": REFERENCES,
        "technologies": TECHNOLOGIES,
    }


def funnel_stats(request):
    """Stats condivise con kesi-site (sezione stats-wave nel funnel)."""
    return {"stats": STATS}
