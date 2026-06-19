"""Modelli per il funnel Grandineticino.ch (lead capture locale)."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class FunnelLead(models.Model):
    """Lead raccolto dal funnel one-page (salvato in SQLite locale)."""

    class DeliveryPreference(models.TextChoices):
        MOBILE = "mobile", _("Servizio Mobile")
        WORKSHOP = "workshop", _("Servizio in Sede (Riazzino)")

    full_name = models.CharField(_("Nome e cognome"), max_length=200, blank=True)
    email = models.EmailField(_("Email"))
    telephone = models.CharField(_("Telefono"), max_length=50)
    city = models.CharField(_("Città"), max_length=100)
    delivery_preference = models.CharField(
        _("Preferenza di appuntamento"),
        max_length=20,
        choices=DeliveryPreference.choices,
    )
    dent_count = models.PositiveSmallIntegerField(_("Numero bolli stimato"), null=True, blank=True)
    damage_details = models.TextField(_("Descrizione del danno"))
    vehicle_details = models.TextField(_("Dati del veicolo"), blank=True)
    source_domain = models.CharField(max_length=100, default="grandineticino.ch")
    utm_source = models.CharField(max_length=200, blank=True)
    utm_medium = models.CharField(max_length=200, blank=True)
    utm_campaign = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=5, default="it")
    email_sent = models.BooleanField(default=False)
    autoresponse_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Lead funnel")
        verbose_name_plural = _("Lead funnel")

    def __str__(self):
        label = self.full_name or self.email
        return f"{label} — {self.created_at:%Y-%m-%d %H:%M}"


class FunnelLeadAttachment(models.Model):
    """Allegato foto associato a un lead funnel."""

    lead = models.ForeignKey(
        FunnelLead,
        related_name="attachments",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="funnel_leads/%Y/%m/")
    original_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Allegato lead")
        verbose_name_plural = _("Allegati lead")

    def __str__(self):
        return self.original_name or self.file.name
