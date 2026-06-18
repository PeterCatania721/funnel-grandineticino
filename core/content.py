"""Contenuti centralizzati del sito KESI SA.

Servizi, vantaggi e clienti tipo, in un punto unico. Le stringhe usano
gettext_lazy così da essere tradotte (IT sorgente, DE/FR/EN nei cataloghi).
Esposti ai template via core.context_processors.site_content.
"""
from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class Service:
    slug: str
    name: object
    description: object
    image: str = ""


@dataclass(frozen=True)
class Advantage:
    title: object
    description: object


@dataclass(frozen=True)
class Target:
    title: object
    description: object
    image: str = ""


@dataclass(frozen=True)
class Stat:
    value: str
    label: object


@dataclass(frozen=True)
class TimelineEntry:
    year: str
    location: object
    description: object


@dataclass(frozen=True)
class Reference:
    name: str
    role: object
    image: str = ""


@dataclass(frozen=True)
class Technology:
    slug: str
    name: object
    tagline: object
    description: object


SERVICES = [
    Service(
        "pdr",
        _("PDR – Levabolli senza verniciatura"),
        _("Rimozione di bolli e ammaccature dalla lamiera senza vernice, "
          "ripristinando la forma originale e preservando la verniciatura di fabbrica."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/67eff89b28ec4c226e0b5495.png",
    ),
    Service(
        "carrozzeria-alternativa",
        _("Carrozzeria alternativa"),
        _("Ripariamo il danno direttamente nel punto colpito, senza rifare il "
          "pezzo e senza verniciatura: meno costi, meno sprechi, stesso risultato."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/6a1d9502f563bf237f803269.jpg",
    ),
    Service(
        "smart-repair",
        _("Smart Repair"),
        _("Riparazione localizzata di graffi, piccoli danni e interni, "
          "combinabile con il PDR per interventi mirati ed economici."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/6a1d94e8bb0618436a46f309.jpg",
    ),
    Service(
        "scanner-ai",
        _("Scanner AI e perizia danni"),
        _("Scannerizzazione professionale con intelligenza artificiale che "
          "individua anche i danni meno visibili, ideale per drive-in e perizie."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/6a1d85e6bb0618436a45ddfc.heic",
    ),
    Service(
        "servizio-mobile",
        _("Servizio mobile in loco"),
        _("Strumenti portatili per intervenire direttamente presso carrozzerie, "
          "concessionari e flotte, in tutta la Svizzera."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/9fd08a7a-f8d3-4efb-a6f3-f9b289923096.jpg",
    ),
    Service(
        "grandi-volumi",
        _("Gestione grandi volumi e flotte"),
        _("Rete di oltre 90 tecnici e sistema digitale dedicato per gestire "
          "picchi stagionali, eventi di grandine e parchi auto numerosi."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/6a1d9cbbd53fc25488ecbb4a.jpg",
    ),
    Service(
        "supporto-team",
        _("Supporto a team PDR esistenti"),
        _("Integriamo e potenziamo i tecnici già attivi nei momenti di maggior "
          "carico, garantendo continuità operativa e tempi ridotti."),
        "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media/6a1d9dca045e32379f3a8a83.jpg",
    ),
]


ADVANTAGES = [
    Advantage(
        _("Vernice originale preservata"),
        _("Manteniamo la verniciatura di fabbrica: estetica intatta e valore del "
          "veicolo protetto, fondamentale su auto d'epoca o di alto valore."),
    ),
    Advantage(
        _("Costi e tempi ridotti"),
        _("Meno passaggi rispetto alla carrozzeria tradizionale: niente "
          "stuccatura, carteggiatura o asciugatura. Danni lievi risolti in tempi brevi."),
    ),
    Advantage(
        _("Soluzione sostenibile"),
        _("Senza vernici, solventi o sostanze chimiche: meno sprechi, meno "
          "impatto ambientale e nessuna cabina di verniciatura necessaria."),
    ),
    Advantage(
        _("Rete di tecnici esperti"),
        _("Oltre 30 anni di esperienza e una rete di professionisti tra i "
          "migliori in Svizzera, Italia, Europa e Stati Uniti."),
    ),
    Advantage(
        _("Copertura in tutta la Svizzera"),
        _("Interveniamo direttamente in loco con strumenti compatti, riducendo "
          "tempi morti, costi logistici e spostamenti dei veicoli."),
    ),
    Advantage(
        _("Etica e trasparenza"),
        _("Lavoriamo con trasparenza verso clienti e assicurazioni, con "
          "gestione tracciabile del danno lungo tutto il processo."),
    ),
]


TARGETS = [
    Target(
        _("Carrozzerie"),
        _("Capacità aggiuntiva nei picchi di lavoro e per i danni più complessi."),
        "https://images.unsplash.com/photo-1618312980096-873bd19759a0?w=480&h=200&fit=crop&q=80",
    ),
    Target(
        _("Concessionari e garage"),
        _("Riparazioni in loco su veicoli nuovi, usati e d'esposizione."),
        "https://images.unsplash.com/photo-1574023240744-64c47c8c0676?w=480&h=200&fit=crop&q=80",
    ),
    Target(
        _("Aziende con flotte"),
        _("Gestione efficiente di grandi numeri di veicoli, con perizie incluse."),
        "https://images.unsplash.com/photo-1587813369290-091c9d432daf?w=480&h=200&fit=crop&q=80",
    ),
    Target(
        _("Assicurazioni"),
        _("Costi di riparazione contenuti e maggiore competitività delle polizze."),
        "/static/img/ref-assicurazioni.jpg",
    ),
]


STATS = [
    Stat("30+", _("Anni di esperienza")),
    Stat("97", _("Tecnici PDR specializzati")),
    Stat("15'250", _("Veicoli riparati in un singolo mandato")),
]


TIMELINE = [
    TimelineEntry("1991", _("Italia – Bergamo"), _("Dopo anni di esperienza come lattoniere in carrozzerie locali, fonda la Carrozzeria P&C a dicembre.")),
    TimelineEntry("1995", _("Italia"), _("Fonda Car Services SRL e sviluppa la tecnica K90: un metodo rivoluzionario PDR senza smontaggio né verniciatura.")),
    TimelineEntry("1998", _("Francia – Parigi"), _("Attività sul piazzale di produzione Citroën.")),
    TimelineEntry("2004", _("Germania – Rastatt"), _("Interventi nello stabilimento Daimler-Chrysler (Mercedes).")),
    TimelineEntry("2007", _("Francia – Flins-sur-Seine"), _("Deposito veicoli nello stabilimento Renault.")),
    TimelineEntry("2008", _("Polonia – Poznań"), _("Attività nello stabilimento Volkswagen.")),
    TimelineEntry("2011", _("Svizzera"), _("AMAG Retail: Audi, Skoda, Volkswagen, Seat. Mercedes a Berna, AMAG a Zurigo.")),
    TimelineEntry("2012", _("Sudafrica – Johannesburg"), _("12 tecnici per BMW Alberante.")),
    TimelineEntry("2015", _("Belgio – Evergem"), _("Riparazione di un piazzale danneggiato dalla grandine.")),
    TimelineEntry("2017", _("Svizzera – Ticino"), _("Oltre 1'000 veicoli riparati in carrozzerie del canton Ticino.")),
    TimelineEntry("2021–2023", _("Svizzera"), _("Espansione in Ticino, San Gallo e Zurigo.")),
    TimelineEntry("2025", _("Svizzera"), _("Attività in Ticino e Sciaffusa. Il network cresce fino a 97 tecnici PDR."))
]


TECHNOLOGIES = [
    Technology(
        "pdr",
        _("PDR – Paintless Dent Repair"),
        _("Rimozione di bolli e ammaccature senza verniciatura"),
        _("La tecnica PDR lavora direttamente sulla lamiera dall'interno, ripristinando la forma originale senza toccare la vernice. Più veloce, più economica e più sostenibile della carrozzeria tradizionale."),
    ),
    Technology(
        "scanner-ai",
        _("Scanner AI portabile"),
        _("Perizie rapide e precise direttamente in loco"),
        _("Il nostro scanner AI portatile rileva con precisione millimetrica danni da grandine e ammaccature anche invisibili a occhio nudo. Ideale per drive-in, concessionari e flotte."),
    ),
    Technology(
        "scanner-360",
        _("Scanner 360° 4-in-1"),
        _("Ispezione completa del veicolo in 15 secondi"),
        _("Postazione fissa con 16 telecamere che scannerizza l'intera superficie esterna, il sottoscocca in 4K, il profilo gomma e i cerchioni in 7K. Report AI dettagliato con millimetro di precisione."),
    ),
    Technology(
        "smart-repair",
        _("Smart Repair"),
        _("Riparazione localizzata di graffi e piccoli danni"),
        _("Intervento mirato su graffi superficiali, piccoli urti e danni agli interni, senza rifare l'intero pannello. Combinabile con il PDR per un risultato completo e rapido."),
    ),
]


REFERENCES = [
    Reference(
        "Carrozzeria Tognetti",
        _("Partner di lunga data per la riparazione danni da grandine"),
        "/static/img/ref-tognetti.jpg",
    ),
    Reference(
        "Carrozzeria Monzeglio",
        _("Partner di lunga data per la riparazione danni da grandine"),
        "/static/img/ref-monzeglio.jpg",
    ),
    Reference(
        "AMAG Retail",
        _("Audi, Skoda, Volkswagen, Seat – Svizzera"),
        "https://dam.amag-group.ch/is/image/amagproduction/amag-autowelt-aussen-9718:4_3_Large?wid=480&hei=200&qlt=82,0&resMode=sharp2",
    ),
    Reference(
        "Centro Porsche Locarno",
        _("Concessionario ufficiale Porsche, Gordola – Ticino"),
        "https://garage-ticino.ch/wp-content/uploads/2023/07/centro-porsche-locarno-garage-concessionario-porsche-gordola-ticino.jpg",
    ),
    Reference(
        "Daimler-Chrysler",
        _("Stabilimento Mercedes, Rastatt – Germania"),
        "https://jesmb.de/wp-content/uploads/2023/11/mercedes-werk-rastatt2.jpg",
    ),
    Reference(
        "Volkswagen",
        _("Stabilimento, Poznań – Polonia"),
        "https://upload.wikimedia.org/wikipedia/commons/2/24/Poznan_Fabryka_Volkswagen_Odlewnia.jpg",
    ),
    Reference(
        "BMW",
        _("Alberante, Johannesburg – Sudafrica"),
        "https://images.unsplash.com/photo-1574023240769-516aad39fabb?w=480&h=200&fit=crop&q=80",
    ),
]
