# Generated by Django 4.1 on 2022-10-25 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='license_number',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
