# Generated by Django 3.0.8 on 2020-11-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0018_status_to_integer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcript',
            name='status',
        ),
    ]
