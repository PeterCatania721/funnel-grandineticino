"""Viste del funnel one-page Grandineticino.ch."""
import json
import logging
from urllib.parse import quote

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
    FUNNEL_WORKSHOP_IMAGE,
    available_grandine_proofs,
)
from core.funnel_forms import FunnelLeadForm, funnel_form_error_state
from core.emailing import send_lead_notification
from core.models import FunnelLead

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
        logger.info(
            "Funnel lead #%s — notifica inviata a %s via backend %s",
            lead.pk,
            settings.LEAD_RECIPIENT_EMAIL,
            settings.EMAIL_BACKEND,
        )
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
            logger.info(
                "Funnel lead #%s — autoresponse inviata a %s",
                lead.pk,
                lead.email,
            )
        except Exception:
            logger.exception("Errore autoresponse lead funnel #%s", lead.pk)

    lead.save(update_fields=["email_sent", "autoresponse_sent"])


def _whatsapp_text() -> str:
    return quote(_("Grandine Ticino - vorrei un preventivo"))


def _funnel_forms(request):
    if request.method == "POST":
        return (
            FunnelLeadForm(request.POST, request.FILES, id_prefix="funnel-"),
            FunnelLeadForm(request.POST, request.FILES, id_prefix="funnel-b-"),
        )
    return (
        FunnelLeadForm(id_prefix="funnel-"),
        FunnelLeadForm(id_prefix="funnel-b-"),
    )


def _error_state_json(form) -> str:
    state = funnel_form_error_state(form)
    return json.dumps(state, ensure_ascii=False) if state else ""


def _funnel_context(request, hero_form=None, bottom_form=None):
    if hero_form is None or bottom_form is None:
        hero_form, bottom_form = _funnel_forms(request)
    return {
        "page_title": _lazy("Riparazione Grandine Ticino"),
        "hero_form": hero_form,
        "bottom_form": bottom_form,
        "hero_form_error_state_json": _error_state_json(hero_form),
        "bottom_form_error_state_json": _error_state_json(bottom_form),
        "funnel_faq": FUNNEL_FAQ,
        "funnel_mistakes": FUNNEL_MISTAKES,
        "funnel_hero_image": FUNNEL_HERO_IMAGE,
        "funnel_workshop_image": FUNNEL_WORKSHOP_IMAGE,
        "funnel_founder_image": FUNNEL_FOUNDER_IMAGE,
        "funnel_brand_logo": FUNNEL_BRAND_LOGO,
        "funnel_proofs": available_grandine_proofs(),
        "whatsapp_text": _whatsapp_text(),
    }


def funnel_grandine(request):
    _capture_utm(request)
    hero_form, bottom_form = _funnel_forms(request)

    if request.method == "POST":
        if hero_form.is_valid():
            lead, saved_attachments = hero_form.save_lead(
                source_domain=request.get_host(),
                language=request.LANGUAGE_CODE or "it",
                utm=_get_utm(request),
            )
            _send_lead_emails(lead, saved_attachments)
            request.session["funnel_lead_id"] = lead.pk
            return redirect("funnel_grazie")

    return render(
        request,
        "pages/funnel/grandine.html",
        _funnel_context(request, hero_form=hero_form, bottom_form=bottom_form),
    )


def funnel_grazie(request):
    lead_id = request.session.pop("funnel_lead_id", None)
    lead = FunnelLead.objects.filter(pk=lead_id).first() if lead_id else None
    return render(request, "pages/funnel/grazie.html", {
        "page_title": _lazy("Grazie — richiesta ricevuta"),
        "lead": lead,
        "whatsapp_text": _whatsapp_text(),
    })
