#!/usr/bin/env python3
"""Verifica invio email SMTP per il funnel (notifica + autoresponse)."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_env_file(path: Path, *, override: bool = False) -> None:
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


def main() -> int:
    load_env_file(ROOT / ".env")
    load_env_file(ROOT / ".env.funnel", override=True)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("FUNNEL_MODE", "true")

    print("== Test invio email funnel ==")
    print(f"PWD: {ROOT}")
    print(f".env presente:        {(ROOT / '.env').is_file()}")
    print(f".env.funnel presente: {(ROOT / '.env.funnel').is_file()}")

    password = os.environ.get("EMAIL_HOST_PASSWORD", "")
    placeholders = {
        "",
        "REPLACE_WITH_YOUR_INFOMANIAK_APP_PASSWORD",
        "INSERISCI-PASSWORD-CASELLA",
        "your-app-password",
        "la-tua-password-infomaniak",
    }
    if password in placeholders:
        print("\n❌ EMAIL_HOST_PASSWORD NON impostata (o è ancora un placeholder).")
        print("   Imposta la password reale Infomaniak per info@kesi.biz in .env o .env.funnel:")
        print("       EMAIL_HOST_PASSWORD=<password-casella>")
        print("   Poi riavvia il container / ./scripts/funnel-dev.")
        return 1

    print(f"EMAIL_HOST_PASSWORD: SET (lunghezza {len(password)})")
    print()

    os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.smtp.EmailBackend"

    import django

    django.setup()

    from django.conf import settings
    from django.core.mail import EmailMessage, send_mail

    recipient = settings.LEAD_RECIPIENT_EMAIL
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT} TLS={settings.EMAIL_USE_TLS}")
    print(f"User: {settings.EMAIL_HOST_USER}")
    print(f"Destinatario lead: {recipient}")
    print()

    try:
        send_mail(
            subject="[TEST] Grandineticino — verifica SMTP",
            message="Email di test dal funnel. Se la ricevi, SMTP funziona.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        print("OK — notifica di test inviata a", recipient)
    except Exception as exc:
        print("ERRORE notifica:", exc)
        return 1

    if settings.FUNNEL_SEND_AUTORESPONSE:
        test_to = os.environ.get("FUNNEL_TEST_AUTORESPONSE_TO", recipient)
        try:
            EmailMessage(
                subject="[TEST] KESI SA — Abbiamo ricevuto la tua richiesta",
                body="Test autoresponse funnel. Configurazione email OK.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_to],
            ).send(fail_silently=False)
            print("OK — autoresponse di test inviata a", test_to)
        except Exception as exc:
            print("ERRORE autoresponse:", exc)
            return 1

    print("\nSMTP configurato correttamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
