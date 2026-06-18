"""Validazione permissiva per numeri di telefono internazionali."""
import re

_PHONE_CHARS = re.compile(r"^[\d\s()+\-./]+$")


def is_valid_phone(value: str) -> bool:
    """Accetta formati IT, CH e internazionali con almeno 6 cifre."""
    value = value.strip()
    if not value or len(value) > 50:
        return False
    if not _PHONE_CHARS.match(value):
        return False
    digits = re.sub(r"\D", "", value)
    return 6 <= len(digits) <= 15
