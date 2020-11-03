# Generated by Django 3.1 on 2020-11-03 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('file_id', models.IntegerField(db_index=True)),
                ('node_id', models.IntegerField(db_index=True)),
                ('tphys', models.FloatField()),
                ('kstar_1', models.FloatField()),
                ('mass0_1', models.FloatField()),
                ('mass_1', models.FloatField()),
                ('lumin_1', models.FloatField()),
                ('rad_1', models.FloatField()),
                ('teff_1', models.FloatField()),
                ('massc_1', models.FloatField()),
                ('radc_1', models.FloatField()),
                ('menv_1', models.FloatField()),
                ('renv_1', models.FloatField()),
                ('epoch_1', models.FloatField()),
                ('ospin_1', models.FloatField()),
                ('deltam_1', models.FloatField()),
                ('rrol_1', models.FloatField()),
                ('kstar_2', models.FloatField()),
                ('mass0_2', models.FloatField()),
                ('mass_2', models.FloatField()),
                ('lumin_2', models.FloatField()),
                ('rad_2', models.FloatField()),
                ('teff_2', models.FloatField()),
                ('massc_2', models.FloatField()),
                ('radc_2', models.FloatField()),
                ('menv_2', models.FloatField()),
                ('renv_2', models.FloatField()),
                ('epoch_2', models.FloatField()),
                ('ospin_2', models.FloatField()),
                ('deltam_2', models.FloatField()),
                ('rrol_2', models.FloatField()),
                ('porb', models.FloatField()),
                ('sep', models.FloatField()),
                ('ecc', models.FloatField()),
                ('b_0_1', models.FloatField()),
                ('b_0_2', models.FloatField()),
                ('snkick_1', models.FloatField()),
                ('snkick_2', models.FloatField()),
                ('vsys_final', models.FloatField()),
                ('sntheta_final', models.FloatField()),
                ('sn_1', models.FloatField()),
                ('sn_2', models.FloatField()),
                ('bin_state', models.FloatField()),
                ('merger_type', models.FloatField()),
                ('bin_num', models.FloatField()),
                ('time_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
