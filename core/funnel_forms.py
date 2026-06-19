"""Form Django per il funnel Grandineticino.ch — unica fonte di verità per i campi."""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import FunnelLead, FunnelLeadAttachment
from core.phone import is_valid_phone

MAX_IMAGES = 15
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

FUNNEL_FORM_STEPS = {
    1: ("full_name", "email", "telephone", "city"),
    2: ("delivery_preference", "images"),
    3: ("damage_details", "vehicle_details", "terms"),
}


def funnel_form_error_state(form) -> dict | None:
    """Stato errori per il wizard client (step iniziale + messaggi per campo)."""
    if not form or not form.errors:
        return None

    fields: dict[str, str] = {}
    first_step: int | None = None

    for step in sorted(FUNNEL_FORM_STEPS):
        for name in FUNNEL_FORM_STEPS[step]:
            if name in form.errors:
                fields[name] = str(form.errors[name][0])
                if first_step is None:
                    first_step = step

    return {"step": first_step or 1, "fields": fields}


class FunnelImageInput(forms.FileInput):
    allow_multiple_selected = True


class FunnelLeadForm(forms.ModelForm):
    """ModelForm per la raccolta lead del funnel one-page."""

    images = forms.Field(
        label=_("Carica foto del danno"),
        required=False,
        widget=FunnelImageInput(
            attrs={
                "accept": ".jpg,.jpeg,.png,.gif",
                "class": "prev-upload-input funnel-upload-input",
                "data-funnel-required": "true",
                "multiple": "multiple",
            }
        ),
    )
    terms = forms.BooleanField(
        label=_(
            "Accetto i termini e acconsento a essere ricontattato per la valutazione del danno."
        ),
        required=True,
        widget=forms.CheckboxInput(),
        error_messages={
            "required": _("Devi accettare i termini per inviare la richiesta."),
        },
    )
    dent_count = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = FunnelLead
        fields = (
            "full_name",
            "email",
            "telephone",
            "city",
            "delivery_preference",
            "damage_details",
            "vehicle_details",
        )
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "prev-input", "placeholder": _("Nome e cognome")},
            ),
            "email": forms.EmailInput(
                attrs={"class": "prev-input", "placeholder": "E-mail"},
            ),
            "telephone": forms.TextInput(
                attrs={
                    "class": "prev-input prev-input--tel",
                    "type": "tel",
                    "inputmode": "tel",
                    "autocomplete": "tel-national",
                    "placeholder": _("79 123 45 67"),
                    "title": _("Numero senza prefisso internazionale"),
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "prev-input",
                    "placeholder": _("Es. Locarno, Lugano, Bellinzona"),
                }
            ),
            "delivery_preference": forms.Select(
                attrs={"class": "prev-input prev-select"},
            ),
            "damage_details": forms.Textarea(
                attrs={
                    "class": "prev-textarea",
                    "rows": 3,
                    "placeholder": _("Quando è successo? Quanti bolli circa?"),
                }
            ),
            "vehicle_details": forms.Textarea(
                attrs={
                    "class": "prev-textarea",
                    "rows": 2,
                    "placeholder": _("Marca, modello, anno"),
                }
            ),
        }

    def __init__(self, *args, id_prefix="", **kwargs):
        super().__init__(*args, **kwargs)
        self.id_prefix = id_prefix

        required_messages = {
            "email": _("Compila tutti i campi obbligatori."),
            "telephone": _("Compila tutti i campi obbligatori."),
            "city": _("Compila tutti i campi obbligatori."),
            "delivery_preference": _("Seleziona la preferenza di appuntamento."),
            "damage_details": _("Compila tutti i campi obbligatori."),
            "images": _("Carica almeno una foto del danno."),
        }
        self.fields["email"].error_messages.setdefault(
            "invalid",
            _("Inserisci un indirizzo email valido."),
        )
        for name, field in self.fields.items():
            if name in required_messages:
                field.error_messages.setdefault("required", required_messages[name])

            widget_id = f"{id_prefix}{name}" if id_prefix else name
            field.widget.attrs.setdefault("id", widget_id)

            step = next((n for n, names in FUNNEL_FORM_STEPS.items() if name in names), None)
            if step is not None:
                field.widget.attrs["data-funnel-step"] = str(step)
            if field.required and not isinstance(field.widget, forms.HiddenInput):
                field.widget.attrs.setdefault("required", "required")

        self.fields["delivery_preference"].choices = [
            ("", _("Seleziona…")),
            *FunnelLead.DeliveryPreference.choices,
        ]
        self.fields["images"].widget.attrs.update({
            "required": "required",
            "data-funnel-required": "true",
        })

    def _uploaded_images(self):
        if not self.files:
            return []
        if hasattr(self.files, "getlist"):
            return self.files.getlist("images")
        uploaded = self.files.get("images")
        if not uploaded:
            return []
        return uploaded if isinstance(uploaded, list) else [uploaded]

    def clean(self):
        cleaned_data = super().clean()
        files = self._uploaded_images()
        if not files:
            self.add_error("images", _("Carica almeno una foto del danno."))
        elif len(files) > MAX_IMAGES:
            self.add_error(
                "images",
                _("Puoi caricare al massimo %(max)s file.") % {"max": MAX_IMAGES},
            )
        else:
            for uploaded in files:
                ext = uploaded.name.rsplit(".", 1)[-1].lower() if "." in uploaded.name else ""
                if (
                    f".{ext}" not in ALLOWED_IMAGE_EXTENSIONS
                    and uploaded.content_type not in ALLOWED_IMAGE_CONTENT_TYPES
                ):
                    self.add_error(
                        "images",
                        _("Formato file non supportato. Usa JPG o PNG."),
                    )
                    break
            if not self.errors.get("images"):
                cleaned_data["images"] = files
        return cleaned_data

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone", "").strip()
        if not telephone:
            raise ValidationError(_("Compila tutti i campi obbligatori."))
        if not is_valid_phone(telephone):
            raise ValidationError(
                _("Inserisci un numero di telefono valido (es. +41 79 123 45 67 o +39 333 123 4567).")
            )
        return telephone

    def clean_dent_count(self):
        raw = (self.cleaned_data.get("dent_count") or "").strip()
        if not raw:
            return None
        if not raw.isdigit():
            raise ValidationError(_("Numero bolli non valido."))
        return int(raw)

    def save_lead(self, *, source_domain, language, utm=None):
        """Crea il lead e gli allegati a partire dai dati validati."""
        utm = utm or {}
        lead = super().save(commit=False)
        lead.source_domain = source_domain
        lead.language = language
        lead.utm_source = utm.get("utm_source", "")
        lead.utm_medium = utm.get("utm_medium", "")
        lead.utm_campaign = utm.get("utm_campaign", "")
        lead.dent_count = self.cleaned_data.get("dent_count")
        lead.save()

        attachments = []
        for uploaded in self.cleaned_data.get("images", []):
            attachments.append(
                FunnelLeadAttachment.objects.create(
                    lead=lead,
                    file=uploaded,
                    original_name=uploaded.name,
                )
            )
        return lead, attachments
