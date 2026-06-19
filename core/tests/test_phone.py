"""Test validazione telefono internazionale."""
from django.test import SimpleTestCase

from core.phone import format_phone, is_valid_phone, normalize_local_digits, split_phone


class PhoneValidationTest(SimpleTestCase):
    def test_swiss_mobile_valid(self):
        self.assertTrue(is_valid_phone("+41 79 123 45 67"))

    def test_swiss_mobile_without_plus(self):
        self.assertTrue(is_valid_phone("79 123 45 67"))

    def test_swiss_mobile_with_trunk_zero(self):
        self.assertTrue(is_valid_phone("+41 079 123 45 67"))

    def test_swiss_mobile_too_short(self):
        self.assertFalse(is_valid_phone("+41 83939383"))
        self.assertFalse(is_valid_phone("83939383"))

    def test_italian_mobile_valid(self):
        self.assertTrue(is_valid_phone("+39 333 123 4567"))

    def test_italian_mobile_too_short(self):
        self.assertFalse(is_valid_phone("+39 333 123 45"))

    def test_invalid_characters(self):
        self.assertFalse(is_valid_phone("abc"))

    def test_split_phone(self):
        self.assertEqual(split_phone("+41 79 123 45 67"), ("+41", "79 123 45 67"))
        self.assertEqual(split_phone("79 123 45 67"), ("+41", "79 123 45 67"))

    def test_normalize_local_digits_strips_trunk_zero(self):
        self.assertEqual(normalize_local_digits("079 123 45 67", "+41"), "791234567")

    def test_format_phone(self):
        self.assertEqual(format_phone("+41", "79 123 45 67"), "+41 79 123 45 67")
