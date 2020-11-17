# Generated by Django 3.0.8 on 2020-11-17 10:37

from django.db import migrations


def status_to_integer(apps, schema_editor):
    Transcript = apps.get_model('analysis', 'Transcript')
    statuses = Transcript._meta.get_field('status_nr').choices
    statuses_dict = {v: k for (k, v) in statuses}

    for transcript in Transcript.objects.all():
        if transcript.status:
            transcript.status_nr = statuses_dict.get(transcript.status, 0)
            transcript.save()


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0017_transcript_status_nr'),
    ]

    operations = [
        migrations.RunPython(status_to_integer),
    ]
