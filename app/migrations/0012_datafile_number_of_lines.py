# Generated by Django 3.1.2 on 2021-04-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210418_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='number_of_lines',
            field=models.PositiveIntegerField(default=0),
        ),
    ]