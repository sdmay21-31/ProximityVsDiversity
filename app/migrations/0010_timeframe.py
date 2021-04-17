# Generated by Django 3.1.2 on 2021-04-17 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210412_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_percentage', models.FloatField(editable=False)),
                ('relativised_nodes', models.JSONField(editable=False)),
                ('dataset', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='app.dataset')),
            ],
            options={
                'db_table': 'timeframe',
                'unique_together': {('dataset', 'time_percentage')},
            },
        ),
    ]
