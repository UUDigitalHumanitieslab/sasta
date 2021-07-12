# Generated by Django 3.1.11 on 2021-06-02 12:28

import logging

from django.db import migrations
from lxml import etree

logger = logging.getLogger('sasta')


def existing_xsid(apps, schema_editor):
    Utterance = apps.get_model('analysis', 'Utterance')
    for utt in Utterance.objects.all():
        syntree = etree.fromstring(utt.parse_tree)
        el = syntree.find('.//meta[@name="xsid"]')
        if el is not None:
            xsid = int(el.attrib['value'])
            utt.xsid = xsid
            utt.save()


def reverse(apps, schema_editor):
    Utterance = apps.get_model('analysis', 'Utterance')
    for utt in Utterance.objects.all():
        utt.xsid = None
        utt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0023_auto_20210602_1428'),
    ]

    operations = [
        migrations.RunPython(existing_xsid, reverse_code=reverse)
    ]