# Generated by Django 3.1.7 on 2021-03-24 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0018_merge_20210128_1224'),
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