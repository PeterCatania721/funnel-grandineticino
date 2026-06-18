"""Viste del funnel one-page Grandineticino.ch."""
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy

from core.funnel_content import (
    FUNNEL_BRAND_LOGO,
    FUNNEL_FAQ,
    FUNNEL_FOUNDER_IMAGE,
    FUNNEL_HERO_IMAGE,
    FUNNEL_MISTAKES,
    FUNNEL_MISTAKES_IMAGE,
    FUNNEL_WORKSHOP_IMAGE,
    available_grandine_proofs,
)
from core.emailing import send_lead_notification
from core.models import FunnelLead, FunnelLeadAttachment
from core.phone import is_valid_phone

logger = logging.getLogger(__name__)


def _capture_utm(request):
    for key in ("utm_source", "utm_medium", "utm_campaign"):
        value = request.GET.get(key, "").strip()
        if value:
            request.session[key] = value[:200]


def _get_utm(request):
    return {
        "utm_source": request.session.get("utm_source", ""),
        "utm_medium": request.session.get("utm_medium", ""),
        "utm_campaign": request.session.get("utm_campaign", ""),
    }


def _send_lead_emails(lead, attachments):
    subject = f"Grandineticino — {lead.full_name or lead.email} — {lead.city}"
    body_lines = [
        "=== NUOVO LEAD GRANDINETICINO.CH ===",
        "",
        f"Nome:            {lead.full_name or '—'}",
        f"Email:           {lead.email}",
        f"Telefono:        {lead.telephone}",
        f"Città:           {lead.city}",
        f"Consegna:        {lead.get_delivery_preference_display() or '—'}",
        f"Bolli stimati:   {lead.dent_count or '—'}",
        f"Lingua:          {lead.language}",
        f"Dominio:         {lead.source_domain}",
        f"UTM source:      {lead.utm_source or '—'}",
        f"UTM medium:      {lead.utm_medium or '—'}",
        f"UTM campaign:    {lead.utm_campaign or '—'}",
        "",
        "--- Descrizione del danno ---",
        lead.damage_details or "—",
        "",
        "--- Dati del veicolo ---",
        lead.vehicle_details or "—",
        "",
        f"Allegati: {len(attachments)} file",
        f"Lead ID: {lead.pk}",
    ]

    try:
        send_lead_notification(
            subject=subject,
            body="\n".join(body_lines),
            reply_to=lead.email,
            attachments=attachments,
        )
        lead.email_sent = True
    except Exception:
        logger.exception("Errore invio email lead funnel #%s", lead.pk)

    if settings.FUNNEL_SEND_AUTORESPONSE:
        try:
            autoresponse = EmailMessage(
                subject=_("KESI SA — Abbiamo ricevuto la tua richiesta"),
                body="\n".join([
                    _("Gentile cliente,"),
                    "",
                    _("Grazie per averci contattato tramite grandineticino.ch."),
                    _("Abbiamo ricevuto le tue foto e i tuoi dati."),
                    _("Ti risponderemo entro 24 ore lavorative con una valutazione gratuita."),
                    "",
                    _("Per urgenze puoi chiamarci al +41 78 967 43 37 o scriverci su WhatsApp."),
                    "",
                    _("Cordiali saluti,"),
                    "KESI SA",
                    "Via Cantonale 42, 6595 Riazzino (Ticino)",
                ]),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[lead.email],
            )
            autoresponse.send()
            lead.autoresponse_sent = True
        except Exception:
            logger.exception("Errore autoresponse lead funnel #%s", lead.pk)

    lead.save(update_fields=["email_sent", "autoresponse_sent"])


def _funnel_context(request, error=None):
    return {
        "page_title": _lazy("Riparazione Grandine Ticino"),
        "error": error,
        "funnel_faq": FUNNEL_FAQ,
        "funnel_mistakes": FUNNEL_MISTAKES,
        "funnel_mistakes_image": FUNNEL_MISTAKES_IMAGE,
        "funnel_hero_image": FUNNEL_HERO_IMAGE,
        "funnel_workshop_image": FUNNEL_WORKSHOP_IMAGE,
        "funnel_founder_image": FUNNEL_FOUNDER_IMAGE,
        "funnel_brand_logo": FUNNEL_BRAND_LOGO,
        "funnel_proofs": available_grandine_proofs(),
        "whatsapp_text": "Grandine%20Ticino%20-%20vorrei%20un%20preventivo",
    }


def funnel_grandine(request):
    _capture_utm(request)
    error = None

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        city = request.POST.get("city", "").strip()
        delivery_preference = request.POST.get("delivery_preference", "").strip()
        damage_details = request.POST.get("damage_details", "").strip()
        vehicle_details = request.POST.get("vehicle_details", "").strip()
        dent_count_raw = request.POST.get("dent_count", "").strip()
        images = request.FILES.getlist("images")
        terms = request.POST.get("terms")

        dent_count = int(dent_count_raw) if dent_count_raw.isdigit() else None

        if not email or not telephone or not city:
            error = _lazy("Compila tutti i campi obbligatori.")
        elif not is_valid_phone(telephone):
            error = _lazy("Inserisci un numero di telefono valido (es. +41 79 123 45 67 o +39 333 123 4567).")
        elif delivery_preference not in FunnelLead.DeliveryPreference.values:
            error = _lazy("Seleziona le preferenze di consegna.")
        elif not terms:
            error = _lazy("Devi accettare i termini per inviare la richiesta.")
        elif not images:
            error = _lazy("Carica almeno una foto del danno.")
        else:
            utm = _get_utm(request)
            lead = FunnelLead.objects.create(
                full_name=full_name,
                email=email,
                telephone=telephone,
                city=city,
                delivery_preference=delivery_preference,
                dent_count=dent_count,
                damage_details=damage_details,
                vehicle_details=vehicle_details,
                source_domain=request.get_host(),
                language=request.LANGUAGE_CODE or "it",
                **utm,
            )
            saved_attachments = []
            for uploaded in images[:15]:
                att = FunnelLeadAttachment.objects.create(
                    lead=lead,
                    file=uploaded,
                    original_name=uploaded.name,
                )
                saved_attachments.append(att)

            _send_lead_emails(lead, saved_attachments)
            request.session["funnel_lead_id"] = lead.pk
            return redirect("funnel_grazie")

    return render(request, "pages/funnel/grandine.html", _funnel_context(request, error=error))


def funnel_grazie(request):
    lead_id = request.session.pop("funnel_lead_id", None)
    lead = FunnelLead.objects.filter(pk=lead_id).first() if lead_id else None
    return render(request, "pages/funnel/grazie.html", {
        "page_title": _lazy("Grazie — richiesta ricevuta"),
        "lead": lead,
    })
