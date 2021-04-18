# Generated by Django 3.1.2 on 2021-04-18 11:39

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_timeframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simulation', models.PositiveIntegerField()),
                ('simulation_index', models.PositiveIntegerField()),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('relativised_data', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('dataset', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='app.dataset')),
            ],
            options={
                'db_table': 'node',
            },
        ),
        migrations.AlterUniqueTogether(
            name='timeframe',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='timeframe',
            name='dataset',
        ),
        migrations.DeleteModel(
            name='Simulation',
        ),
        migrations.DeleteModel(
            name='TimeFrame',
        ),
    ]