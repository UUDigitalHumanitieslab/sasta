# Generated by Django 3.0.8 on 2021-01-28 10:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0016_auto_20200921_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus',
            name='date_added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corpus',
            name='date_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='date_added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
