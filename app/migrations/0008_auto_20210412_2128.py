# Generated by Django 3.1.2 on 2021-04-12 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210412_2057'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DatasetFile',
            new_name='DataFile',
        ),
    ]
