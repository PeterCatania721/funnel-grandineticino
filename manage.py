#!/usr/bin/env python
"""Django command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossibile importare Django. Verifica che sia installato e "
            "che l'ambiente virtuale sia attivo."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
