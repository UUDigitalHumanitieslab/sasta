# Generated by Django 3.1.12 on 2021-07-20 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0024_xsid_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='corrections',
            field=models.JSONField(blank=True, null=True),
        ),
    ]