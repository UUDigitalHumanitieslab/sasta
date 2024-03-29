# Generated by Django 3.1.14 on 2022-07-26 11:10

import analysis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0030_transcript_corrected_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisrun',
            name='annotation_file',
            field=models.FileField(max_length=500, upload_to=analysis.models.AnalysisRun.upload_path),
        ),
        migrations.AlterField(
            model_name='analysisrun',
            name='query_file',
            field=models.FileField(max_length=500, upload_to=analysis.models.AnalysisRun.upload_path),
        ),
        migrations.AlterField(
            model_name='assessmentmethod',
            name='content',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=analysis.models.AssessmentMethod.upload_path),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='content',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=analysis.models.Transcript.upload_path),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='corrected_content',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=analysis.models.Transcript.upload_path_parsed),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='parsed_content',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=analysis.models.Transcript.upload_path_parsed),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='content',
            field=models.FileField(max_length=500, upload_to=analysis.models.UploadFile.upload_path),
        ),
    ]
