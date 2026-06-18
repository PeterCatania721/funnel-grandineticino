from core.company import COMPANY
from core.content import STATS


def company(request):
    """Espone i dati aziendali a tutti i template come `company`."""
    return {"company": COMPANY}


def funnel_stats(request):
    """Stats condivise con kesi-site (sezione stats-wave nel funnel)."""
    return {"stats": STATS}
