# Generated by Django 4.1 on 2023-04-26 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
