# Generated by Django 3.1.11 on 2021-06-02 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0022_rename_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='target_ids',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transcript',
            name='target_speakers',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='utterance',
            name='xsid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
