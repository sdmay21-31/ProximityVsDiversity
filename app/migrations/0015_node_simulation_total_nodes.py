# Generated by Django 3.1.2 on 2021-04-20 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210418_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='simulation_total_nodes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
