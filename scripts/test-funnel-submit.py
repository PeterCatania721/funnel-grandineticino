#!/usr/bin/env python3
"""Test end-to-end del form funnel contro il server locale."""
import re
import sys
from io import BytesIO
from urllib.parse import urljoin

import requests

BASE = "http://localhost:8001/it/"
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f"
    b"\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


def main():
    session = requests.Session()

    print("1. GET pagina funnel…")
    r = session.get(BASE, timeout=10)
    r.raise_for_status()
    if "funnelFormWizard" not in r.text:
        print("FAIL: wizard JS non trovato nella pagina")
        return 1

    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text)
    if not m:
        print("FAIL: token CSRF non trovato")
        return 1
    csrf = m.group(1)
    print("   OK — pagina caricata, CSRF ottenuto")

    payload = {
        "csrfmiddlewaretoken": csrf,
        "full_name": "Test Agent",
        "email": "test-agent@example.com",
        "telephone": "+41 79 999 88 77",
        "city": "Bellinzona",
        "delivery_preference": "workshop",
        "damage_details": "Test automatico form multi-step",
        "vehicle_details": "VW Golf 2020",
        "terms": "on",
        "dent_count": "",
    }
    files = [
        ("images", ("test-hail.png", BytesIO(_TINY_PNG), "image/png")),
    ]

    print("2. POST form completo (tutti i campi, come submit step 3)…")
    r = session.post(
        BASE,
        data=payload,
        files=files,
        headers={"Referer": BASE},
        allow_redirects=False,
        timeout=15,
    )

    if r.status_code != 302:
        print(f"FAIL: atteso redirect 302, ricevuto {r.status_code}")
        print(r.text[:500])
        return 1

    location = r.headers.get("Location", "")
    if "/grazie/" not in location:
        print(f"FAIL: redirect inatteso → {location}")
        return 1
    print(f"   OK — redirect a {location}")

    grazie_url = urljoin(BASE, location)
    r2 = session.get(grazie_url, timeout=10)
    r2.raise_for_status()
    if "Richiesta inviata" not in r2.text:
        print("FAIL: pagina grazie senza conferma")
        return 1
    print("   OK — pagina grazie mostrata")

    print("\nTutti i controlli HTTP superati.")
    print("Verifica email: controlla i log del server (console backend in dev).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
