# Generated by Django 3.1.2 on 2021-04-06 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='simulation_attributes',
            new_name='attributes',
        ),
    ]
