from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_funnellead_delivery_preference"),
    ]

    operations = [
        migrations.AlterField(
            model_name="funnellead",
            name="damage_details",
            field=models.TextField(verbose_name="Descrizione del danno"),
        ),
        migrations.AlterField(
            model_name="funnellead",
            name="delivery_preference",
            field=models.CharField(
                choices=[
                    ("mobile", "Servizio Mobile"),
                    ("workshop", "Servizio in Sede (Riazzino)"),
                ],
                max_length=20,
                verbose_name="Preferenza di appuntamento",
            ),
        ),
    ]
