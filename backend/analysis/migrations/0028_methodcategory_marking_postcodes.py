# Generated by Django 3.1.12 on 2021-12-17 13:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0027_analysisrun'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodcategory',
            name='marking_postcodes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), default=list, size=None),
        ),
    ]
