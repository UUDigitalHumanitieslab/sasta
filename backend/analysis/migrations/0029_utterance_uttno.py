# Generated by Django 3.1.13 on 2022-02-01 09:28

from django.db import migrations, models
from lxml import etree


def set_default_uttno(apps, schema_editor):
    Utterance = apps.get_model('analysis', 'Utterance')
    for utterance in Utterance.objects.all().iterator():
        if not utterance.uttno:
            if utterance.parse_tree:
                syntree = etree.fromstring(utterance.parse_tree)
                el = syntree.find('.//meta[@name="uttno"]')
                if el is not None:
                    utterance.uttno = int(el.attrib['value'])
                    utterance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0028_methodcategory_marking_postcodes'),
    ]

    operations = [
        # Initially set as nullable to allow custom default value
        migrations.AddField(
            model_name='utterance',
            name='uttno',
            field=models.IntegerField(null=True),
        ),
        # Set default
        migrations.RunPython(set_default_uttno, reverse_code=migrations.RunPython.noop),
        # And remove nullable
        migrations.AlterField(model_name='utterance',
                              name='uttno',
                              field=models.IntegerField()
                              )
    ]