# Generated by Django 4.2.7 on 2023-11-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taxi", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manufacturer",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
