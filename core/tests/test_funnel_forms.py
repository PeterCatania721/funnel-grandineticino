"""Test unitari per FunnelLeadForm."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from core.funnel_forms import FunnelLeadForm, funnel_form_error_state

_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f"
    b"\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


class FunnelLeadFormTest(SimpleTestCase):
    def _valid_data(self):
        return {
            "full_name": "Mario Rossi",
            "email": "mario@example.com",
            "telephone": "+41 79 123 45 67",
            "city": "Locarno",
            "delivery_preference": "mobile",
            "damage_details": "Grandine sul cofano, circa 15 bolli.",
            "vehicle_details": "BMW Serie 3, 2019",
            "terms": True,
        }

    def test_required_fields_marked_on_widgets(self):
        form = FunnelLeadForm(id_prefix="funnel-")
        for name in ("email", "telephone", "city", "delivery_preference", "damage_details", "terms"):
            self.assertTrue(form.fields[name].required)
            if name != "terms":
                self.assertIn("required", form.fields[name].widget.attrs)

    def test_damage_details_required(self):
        data = self._valid_data()
        data["damage_details"] = ""
        form = FunnelLeadForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("damage_details", form.errors)

    def test_valid_form_accepts_payload(self):
        image = SimpleUploadedFile("damage.png", _TINY_PNG, content_type="image/png")
        form = FunnelLeadForm(data=self._valid_data(), files={"images": image})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_email_shows_translated_error(self):
        from django.utils import translation

        data = self._valid_data()
        data["email"] = "not-an-email"
        with translation.override("de"):
            form = FunnelLeadForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn("email", form.errors)
            self.assertIn("gültige E-Mail-Adresse", form.errors["email"][0])

    def test_too_many_images_shows_translated_error(self):
        from django.utils import translation

        images = [
            SimpleUploadedFile(f"damage-{i}.png", _TINY_PNG, content_type="image/png")
            for i in range(16)
        ]
        with translation.override("fr"):
            form = FunnelLeadForm(data=self._valid_data(), files={"images": images})
            self.assertFalse(form.is_valid())
            self.assertIn("images", form.errors)
            self.assertIn("15 fichiers", form.errors["images"][0])

    def test_invalid_file_type_shows_translated_error(self):
        from django.utils import translation

        bad_file = SimpleUploadedFile("damage.txt", b"not an image", content_type="text/plain")
        with translation.override("en"):
            form = FunnelLeadForm(data=self._valid_data(), files={"images": bad_file})
            self.assertFalse(form.is_valid())
            self.assertIn("images", form.errors)
            self.assertIn("Unsupported file format", form.errors["images"][0])
            self.assertIn("images only", form.errors["images"][0].lower())

    def test_rejects_pdf_and_documents(self):
        for name, ctype in (
            ("report.pdf", "application/pdf"),
            ("notes.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("sheet.csv", "text/csv"),
        ):
            bad = SimpleUploadedFile(name, b"%PDF-1.4 fake", content_type=ctype)
            form = FunnelLeadForm(data=self._valid_data(), files={"images": bad})
            self.assertFalse(form.is_valid(), name)
            self.assertIn("images", form.errors)

    def test_accepts_common_phone_camera_image_types(self):
        cases = (
            ("photo.jpg", "image/jpeg"),
            ("photo.JPEG", "image/jpeg"),
            ("photo.png", "image/png"),
            ("photo.webp", "image/webp"),
            ("photo.heic", "image/heic"),
            ("photo.heif", "image/heif"),
            ("photo.gif", "image/gif"),
            ("photo.bmp", "image/bmp"),
            ("photo.tif", "image/tiff"),
            ("photo.avif", "image/avif"),
            # iOS often leaves content_type empty; extension must still pass
            ("IMG_0001.HEIC", ""),
        )
        for name, ctype in cases:
            uploaded = SimpleUploadedFile(name, _TINY_PNG, content_type=ctype or "application/octet-stream")
            form = FunnelLeadForm(data=self._valid_data(), files={"images": uploaded})
            self.assertTrue(form.is_valid(), f"{name}: {form.errors}")

    def test_images_widget_accept_is_images_only(self):
        form = FunnelLeadForm()
        accept = form.fields["images"].widget.attrs.get("accept", "")
        self.assertIn("image/*", accept)
        self.assertIn(".heic", accept)
        self.assertNotIn(".pdf", accept)
        self.assertNotIn(".doc", accept)

    def test_error_state_maps_fields_to_step(self):
        image = SimpleUploadedFile("damage.png", _TINY_PNG, content_type="image/png")
        data = self._valid_data()
        data["damage_details"] = ""
        data["terms"] = False
        form = FunnelLeadForm(data=data, files={"images": image})
        self.assertFalse(form.is_valid())
        state = funnel_form_error_state(form)
        self.assertEqual(state["step"], 3)
        self.assertIn("damage_details", state["fields"])
