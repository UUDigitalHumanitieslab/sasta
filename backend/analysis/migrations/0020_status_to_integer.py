# Generated by Django 3.1.11 on 2021-06-02 10:06

from django.db import migrations


def status_to_integer(apps, schema_editor):
    Transcript = apps.get_model('analysis', 'Transcript')
    statuses = Transcript._meta.get_field('status_nr').choices
    statuses_dict = {v: k for (k, v) in statuses}

    for transcript in Transcript.objects.all():
        if transcript.status:
            transcript.status_nr = statuses_dict.get(transcript.status, 0)
            transcript.save()


def status_from_integer(apps, schema_editor):
    Transcript = apps.get_model('analysis', 'Transcript')
    statuses = Transcript._meta.get_field('status_nr').choices
    statuses_reverse_dict = {k: v for (k, v) in statuses}

    for transcript in Transcript.objects.all():
        if transcript.status_nr:
            transcript.status = statuses_reverse_dict.get(transcript.status_nr, 'unknown')
            transcript.save()


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0019_transcript_status_nr'),
    ]

    operations = [
        migrations.RunPython(status_to_integer, reverse_code=status_from_integer)
    ]
