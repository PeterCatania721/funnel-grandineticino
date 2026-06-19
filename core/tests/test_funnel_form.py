"""Test invio form funnel e email lead."""
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from core.models import FunnelLead

# Minimal valid 1x1 PNG
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f"
    b"\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _tiny_png(name="test-damage.png"):
    return SimpleUploadedFile(name, _TINY_PNG, content_type="image/png")


_TEST_SETTINGS = {
    "FUNNEL_MODE": True,
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "FUNNEL_SEND_AUTORESPONSE": True,
    "LEAD_RECIPIENT_EMAIL": "info@kesi.biz",
    "DEFAULT_FROM_EMAIL": "info@kesi.biz",
    "STORAGES": {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
}


@override_settings(**_TEST_SETTINGS)
class FunnelFormSubmitTest(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")

    def _valid_payload(self):
        return {
            "full_name": "Mario Rossi",
            "email": "mario.rossi@example.com",
            "telephone": "+41 79 123 45 67",
            "city": "Locarno",
            "delivery_preference": "mobile",
            "damage_details": "Grandine ieri sera, circa 20 bolli sul cofano.",
            "vehicle_details": "BMW Serie 3, 2019",
            "terms": "on",
        }

    def test_successful_submit_creates_lead_and_sends_emails(self):
        mail.outbox.clear()
        image = _tiny_png()

        response = self.client.post(
            "/it/",
            {**self._valid_payload(), "images": image},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/it/grazie/", response["Location"])

        lead = FunnelLead.objects.get(email="mario.rossi@example.com")
        self.assertEqual(lead.full_name, "Mario Rossi")
        self.assertEqual(lead.city, "Locarno")
        self.assertEqual(lead.delivery_preference, "mobile")
        self.assertTrue(lead.email_sent)
        self.assertTrue(lead.autoresponse_sent)
        self.assertEqual(lead.attachments.count(), 1)

        self.assertEqual(len(mail.outbox), 2)

        notification = mail.outbox[0]
        self.assertEqual(notification.to, ["info@kesi.biz"])
        self.assertIn("Grandineticino", notification.subject)
        self.assertIn("Mario Rossi", notification.body)
        self.assertIn("Locarno", notification.body)
        self.assertEqual(notification.reply_to, ["mario.rossi@example.com"])
        self.assertEqual(len(notification.attachments), 1)

        autoresponse = mail.outbox[1]
        self.assertEqual(autoresponse.to, ["mario.rossi@example.com"])
        self.assertIn("ricevuto", autoresponse.subject.lower())

    def test_missing_required_fields_shows_error(self):
        mail.outbox.clear()
        response = self.client.post(
            "/it/",
            {
                "email": "",
                "telephone": "",
                "city": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compila tutti i campi obbligatori")
        self.assertEqual(FunnelLead.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_images_shows_error(self):
        mail.outbox.clear()
        response = self.client.post("/it/", self._valid_payload())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carica almeno una foto del danno")
        self.assertEqual(FunnelLead.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_phone_shows_error(self):
        mail.outbox.clear()
        payload = self._valid_payload()
        payload["telephone"] = "abc"
        response = self.client.post(
            "/it/",
            {**payload, "images": _tiny_png()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "numero di telefono valido")
        self.assertEqual(FunnelLead.objects.count(), 0)

    def test_short_phone_shows_error(self):
        mail.outbox.clear()
        payload = self._valid_payload()
        payload["telephone"] = "+41 83939383"
        response = self.client.post(
            "/it/",
            {**payload, "images": _tiny_png()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "numero di telefono valido")
        self.assertEqual(FunnelLead.objects.count(), 0)

    def test_grazie_page_after_submit(self):
        image = _tiny_png()
        response = self.client.post(
            "/it/",
            {**self._valid_payload(), "images": image},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Richiesta inviata")

    def test_missing_damage_details_shows_error(self):
        mail.outbox.clear()
        payload = self._valid_payload()
        payload["damage_details"] = ""
        response = self.client.post(
            "/it/",
            {**payload, "images": _tiny_png()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compila tutti i campi obbligatori")
        self.assertContains(response, "data-funnel-server-state")
        self.assertContains(response, "damage_details")
        self.assertEqual(FunnelLead.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_email_shows_error(self):
        mail.outbox.clear()
        payload = self._valid_payload()
        payload["email"] = "not-an-email"
        response = self.client.post(
            "/it/",
            {**payload, "images": _tiny_png()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "indirizzo email valido")
        self.assertEqual(FunnelLead.objects.count(), 0)

    def test_funnel_page_translated_for_all_languages(self):
        snippets = {
            "de": ("Sparen Sie bis zu 70 %", "KOSTENLOSE ANFRAGE SENDEN"),
            "fr": ("Économisez jusqu", "ENVOYER LA DEMANDE GRATUITE"),
            "en": ("Save up to 70%", "SEND FREE REQUEST"),
        }
        for lang, (hero, submit) in snippets.items():
            with self.subTest(lang=lang):
                response = self.client.get(f"/{lang}/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, hero)
                self.assertContains(response, submit)
                self.assertContains(response, 'lang-code">{}'.format(lang.upper()))

    def test_error_messages_translated_per_language(self):
        error_snippets = {
            "de": "Füllen Sie alle Pflichtfelder aus",
            "fr": "Remplissez tous les champs obligatoires",
            "en": "Fill in all required fields",
        }
        for lang, snippet in error_snippets.items():
            with self.subTest(lang=lang):
                response = self.client.post(
                    f"/{lang}/",
                    {"email": "", "telephone": "", "city": ""},
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, snippet)

    def test_missing_damage_details_error_translated(self):
        payload = self._valid_payload()
        payload["damage_details"] = ""
        response = self.client.post(
            "/de/",
            {**payload, "images": _tiny_png()},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Füllen Sie alle Pflichtfelder aus")
