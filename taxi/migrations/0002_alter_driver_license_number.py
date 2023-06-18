# Generated by Django 4.1 on 2023-06-18 11:35

from django.db import migrations, models
import taxi.models


class Migration(migrations.Migration):
    dependencies = [
        ("taxi", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="license_number",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[taxi.models.validator_license_number],
            ),
        ),
    ]
