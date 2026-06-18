# Generated manually for funnel MVP

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FunnelLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(blank=True, max_length=200, verbose_name="Nome e cognome")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("telephone", models.CharField(max_length=50, verbose_name="Telefono")),
                ("city", models.CharField(max_length=100, verbose_name="Città")),
                ("dent_count", models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Numero bolli stimato")),
                ("damage_details", models.TextField(blank=True, verbose_name="Descrizione del danno")),
                ("vehicle_details", models.TextField(blank=True, verbose_name="Dati del veicolo")),
                ("source_domain", models.CharField(default="grandineticino.ch", max_length=100)),
                ("utm_source", models.CharField(blank=True, max_length=200)),
                ("utm_medium", models.CharField(blank=True, max_length=200)),
                ("utm_campaign", models.CharField(blank=True, max_length=200)),
                ("language", models.CharField(default="it", max_length=5)),
                ("email_sent", models.BooleanField(default=False)),
                ("autoresponse_sent", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Lead funnel",
                "verbose_name_plural": "Lead funnel",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="FunnelLeadAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="funnel_leads/%Y/%m/")),
                ("original_name", models.CharField(blank=True, max_length=255)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="core.funnellead",
                    ),
                ),
            ],
            options={
                "verbose_name": "Allegato lead",
                "verbose_name_plural": "Allegati lead",
            },
        ),
    ]
