# Generated by Django 4.1 on 2023-08-07 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='license_number',
            field=models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a value with 3 uppercase letters followed by 5 digits.', regex='^[A-Z]{3}\\d{5}$'), django.core.validators.MinLengthValidator(8)]),
        ),
    ]
