from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_funnel_lead"),
    ]

    operations = [
        migrations.AddField(
            model_name="funnellead",
            name="delivery_preference",
            field=models.CharField(
                blank=True,
                choices=[
                    ("mobile", "Servizio Mobile"),
                    ("workshop", "Servizio in Sede (Riazzino)"),
                ],
                max_length=20,
                verbose_name="Preferenze di consegna",
            ),
        ),
    ]
