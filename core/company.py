"""Dati aziendali centralizzati di KESI SA.

Punto unico di verità per nome, contatti e riferimenti. I template li usano
tramite il context processor `core.context_processors.company` come `company`.

NOTA: i campi marcati TODO vanno completati con i dati ufficiali.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Company:
    legal_name: str = "KESI SA"
    short_name: str = "KESI"
    tagline: str = "Carrozzeria alternativa · PDR · Smart Repair"

    # Indirizzo
    street: str = "Via Cantonale 42"
    postal_code: str = "6595"
    city: str = "Riazzino"
    canton: str = "Ticino"
    country: str = "Svizzera"

    # Area di servizio
    service_area: str = "Tutta la Svizzera"

    # Contatti
    phone: str = "+41 78 967 43 37"
    phone_href: str = "+41789674337"
    email: str = "info@kesi.biz"

    # Web
    domain: str = "kesi-automotive.ch"
    website: str = "https://kesi-automotive.ch"

    # Dati amministrativi
    vat: str = ""  # TODO: numero IVA / IDE

    # Social (lasciare vuoto se non presente)
    social: dict = field(default_factory=dict)

    @property
    def address_line(self) -> str:
        parts = [self.street, f"{self.postal_code} {self.city}".strip(), self.country]
        return ", ".join(p for p in parts if p)


COMPANY = Company()
