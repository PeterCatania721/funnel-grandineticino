"""Validazione numeri di telefono internazionali con regole per prefisso."""
import re

_PHONE_CHARS = re.compile(r"^[\d\s()+\-./]+$")

# Ordine decrescente per match corretto (+423 prima di +42).
DIAL_CODES = ("+423", "+41", "+39", "+49", "+33", "+43", "+44", "+1")

# Lunghezza cifre nazionali (senza prefisso internazionale, senza 0 iniziale).
LOCAL_DIGIT_RULES: dict[str, tuple[int, int]] = {
    "+41": (9, 9),
    "+39": (9, 10),
    "+49": (10, 11),
    "+33": (9, 9),
    "+43": (10, 13),
    "+423": (7, 9),
    "+44": (10, 10),
    "+1": (10, 10),
}

_DEFAULT_LOCAL = (8, 12)


def split_phone(value: str) -> tuple[str, str]:
    """Separa prefisso internazionale e numero locale."""
    trimmed = (value or "").strip()
    if not trimmed:
        return "+41", ""

    normalized = re.sub(r"\s+", "", trimmed)
    if not normalized.startswith("+"):
        return "+41", trimmed

    for code in DIAL_CODES:
        if normalized.startswith(code):
            local = trimmed[normalized.index(code) + len(code):].strip()
            return code, local

    return "+41", trimmed


def normalize_local_digits(local: str, code: str) -> str:
    """Rimuove caratteri non numerici e lo 0 iniziale nazionale se presente."""
    digits = re.sub(r"\D", "", local or "")
    if code in ("+41", "+39", "+43", "+49", "+33", "+423") and digits.startswith("0"):
        digits = digits[1:]
    return digits


def format_phone(code: str, local: str) -> str:
    """Combina prefisso e numero locale per l'invio al server."""
    local = (local or "").strip()
    if not local:
        return ""
    if local.startswith("+"):
        return local
    return f"{code} {local}"


def is_valid_phone(value: str) -> bool:
    """Valida il numero completo o solo la parte locale (default +41)."""
    value = (value or "").strip()
    if not value or len(value) > 50:
        return False
    if not _PHONE_CHARS.match(value):
        return False

    code, local = split_phone(value)
    if not local and value.startswith("+"):
        return False

    digits = normalize_local_digits(local, code)
    if not digits or not digits.isdigit():
        return False

    min_len, max_len = LOCAL_DIGIT_RULES.get(code, _DEFAULT_LOCAL)
    if not (min_len <= len(digits) <= max_len):
        return False

    if digits[0] == "0":
        return False

    return True
