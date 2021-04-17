# Generated by Django 3.1.2 on 2021-04-12 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210412_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.IntegerField(choices=[(0, 'Created'), (1, 'Seeding'), (2, 'Completed'), (3, 'Error'), (4, 'Legacy')], default=4),
        ),
    ]
