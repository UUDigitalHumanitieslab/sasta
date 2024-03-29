# Generated by Django 3.0a1 on 2020-03-09 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_corpus_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcript',
            name='corpus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcripts', to='analysis.Corpus'),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='corpus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='analysis.Corpus'),
        ),
    ]
