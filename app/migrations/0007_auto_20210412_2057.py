# Generated by Django 3.1.2 on 2021-04-12 20:57

import autoslug.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_dataset_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('file', models.FileField(upload_to='datasets', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xls'])])),
            ],
            options={
                'db_table': 'dataset_file',
            },
        ),
        migrations.AddField(
            model_name='dataset',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.datasetfile'),
        ),
    ]