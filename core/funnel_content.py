"""Contenuti e asset del funnel Grandineticino.ch.

Le immagini e i video provengono dal CDN Go High Level (filesafe.space),
già usato sul sito principale KESI. Aggiornare gli URL qui senza toccare i template.
"""
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.utils.translation import gettext_lazy as _

GHL = "https://assets.cdn.filesafe.space/2WBwyq6vtWDbHIdzNpFi/media"

# Asset principali del funnel
FUNNEL_HERO_IMAGE = f"{GHL}/67ebba0913c4b653f81b5bf3.jpeg"
FUNNEL_WORKSHOP_IMAGE = f"{GHL}/6a1d94f11f28836ddfc365a2.jpg"
FUNNEL_FOUNDER_IMAGE = "/static/img/kesi-founder.jpg"
FUNNEL_VIDEO_POSTER = f"{GHL}/67ebd8c9-5b39-4b26-a4e8-631a2ac9cccb.jpg"
FUNNEL_VIDEO_MP4 = f"{GHL}/cd9cc4e6-0261-4239-93d5-4c225b3d1f8f.mp4"

FUNNEL_BRAND_LOGO = f"{GHL}/67eff89b28ec4c226e0b5495.png"
FUNNEL_MISTAKES_IMAGE = "img/before-grandine-1.jpg"


@dataclass(frozen=True)
class BeforeAfterPair:
    """Coppia prima/dopo — path relativi a static/ (es. img/before-grandine-1.jpg)."""

    before: str
    after: str
    before_alt: object
    after_alt: object


FUNNEL_GRANDINE_PROOFS = (
    BeforeAfterPair(
        before="img/before-grandine-1.jpg",
        after="img/after-grandine-1.jpg",
        before_alt=_("Prima: danni da grandine con marcature PDR"),
        after_alt=_("Dopo: riparazione PDR in officina KESI"),
    ),
    BeforeAfterPair(
        before="img/before-grandine-2.jpg",
        after="img/after-grandine-2.jpg",
        before_alt=_("Prima: ammaccature da grandine sul parafango"),
        after_alt=_("Dopo: parafango ripristinato senza verniciatura"),
    ),
)

# Backward-compatible alias (prima coppia)
FUNNEL_GRANDINE_PROOF = FUNNEL_GRANDINE_PROOFS[0]


def available_grandine_proofs():
    """Return only pairs whose JPG files exist in static/img/."""
    img_dir = Path(settings.BASE_DIR) / "static" / "img"
    available = []
    for proof in FUNNEL_GRANDINE_PROOFS:
        before = img_dir / proof.before.removeprefix("img/")
        after = img_dir / proof.after.removeprefix("img/")
        if before.is_file() and after.is_file():
            available.append(proof)
    return available


@dataclass(frozen=True)
class FunnelFaq:
    question: object
    answer: tuple  # paragrafi della risposta (gettext_lazy)


@dataclass(frozen=True)
class FunnelValueItem:
    title: object
    description: object


FUNNEL_FAQ = [
    FunnelFaq(
        _("PDR?"),
        (
            _("PDR significa Paintless Dent Repair: levabolli senza verniciatura."),
        ),
    ),
    FunnelFaq(
        _("La vernice resta intatta?"),
        (
            _("Sì. Il PDR lavora sulla lamiera senza verniciare: la vernice di fabbrica "
              "resta originale e il valore del veicolo è protetto."),
            _("Dipende però dall'entità del danno: contattaci per una consulenza gratuita. "
              "Come carrozzieri professionisti ti diciamo se la tua auto grandinata è "
              "riparabile senza verniciatura."),
        ),
    ),
    FunnelFaq(
        _("Quanto costa rispetto alla carrozzeria tradizionale?"),
        (
            _("In media il PDR costa dal 40% al 70% in meno rispetto a verniciatura e "
              "sostituzione pannelli, con tempi molto più brevi."),
            _("Si tratta di un risparmio indicativo, calcolato sul confronto con una "
              "riparazione tradizionale con verniciatura rispetto a un intervento senza "
              "riverniciatura eseguito da tecnici esperti in danni da grandine."),
        ),
    ),
    FunnelFaq(
        _("L'assicurazione copre i danni da grandine?"),
        (
            _("In Svizzera i danni da grandine sono generalmente coperti dalla casco."),
            _("Verifichiamo noi se il tuo veicolo è coperto: con la foto della carta grigia "
              "possiamo gestire la pratica per tuo conto."),
            _("Se è prevista una franchigia, te la comunichiamo subito così ci mettiamo "
              "d'accordo nel migliore dei modi."),
        ),
    ),
    FunnelFaq(
        _("Quanto tempo ci vuole?"),
        (
            _("Molti interventi si completano da 1 a 3 giorni, contro settimane in "
              "carrozzeria tradizionale."),
        ),
    ),
    FunnelFaq(
        _("Dove intervenite in Ticino?"),
        (
            _("Sede a Riazzino e servizio mobile in tutto il canton Ticino e in tutta la "
              "Svizzera."),
        ),
    ),
]


FUNNEL_VALUE_STACK = [
    FunnelValueItem(
        _("Valutazione foto gratuita"),
        _("Risposta entro 24 ore lavorative con stima personalizzata."),
    ),
    FunnelValueItem(
        _("Confronto costi trasparente"),
        _("Stima PDR vs carrozzeria tradizionale, senza sorprese."),
    ),
    FunnelValueItem(
        _("Supporto assicurazione"),
        _("Ti aiutiamo con foto e documentazione per la perizia."),
    ),
    FunnelValueItem(
        _("Intervento mobile"),
        _("Possiamo intervenire presso la tua carrozzeria o a domicilio in Ticino."),
    ),
]


FUNNEL_MISTAKES = [
    _("Aspettare settimane prima di fare il preventivo: l'auto potrebbe andare in danno totale in caso di grandinata o danno aggiuntivo"),
    _("Non sapere chi ripara la vostra macchina grandinata: KESI è una garanzia"),
    _("Non fotografare tutti i bolli prima di portare l'auto in carrozzeria."),
    _("Non verificare la copertura assicurativa per danni da grandine."),
    _("Scegliere il preventivo più basso senza controllare la qualità del lavoro."),
]
