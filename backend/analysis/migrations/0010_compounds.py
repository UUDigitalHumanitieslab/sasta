# Generated by Django 3.0a1 on 2020-03-31 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0009_assessmentquery_inform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HeadDiaNew', models.CharField(max_length=100)),
                ('FlatClass', models.CharField(max_length=100)),
                ('Class', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompoundFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to='files/compoundfiles')),
            ],
        ),
    ]