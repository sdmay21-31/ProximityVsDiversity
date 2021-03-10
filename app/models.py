from django.db import models


# Put query functions here
class NodeQuerySet(models.QuerySet):
    def example_query(self, *args, **kwargs):
        """ Filter time_id is less than or equeal to 200"""
        return self.filter(time_id__lte=200)


# Put class based attributes here
class Node(models.Model):
    file_id = models.IntegerField(db_index=True)
    node_id = models.IntegerField(db_index=True)
    tphys = models.FloatField()
    kstar_1 = models.FloatField()
    mass0_1 = models.FloatField()
    mass_1 = models.FloatField()
    lumin_1 = models.FloatField()
    rad_1 = models.FloatField()
    teff_1 = models.FloatField()
    massc_1 = models.FloatField()
    radc_1 = models.FloatField()
    menv_1 = models.FloatField()
    renv_1 = models.FloatField()
    epoch_1 = models.FloatField()
    ospin_1 = models.FloatField()
    deltam_1 = models.FloatField()
    rrol_1 = models.FloatField()
    kstar_2 = models.FloatField()
    mass0_2 = models.FloatField()
    mass_2 = models.FloatField()
    lumin_2 = models.FloatField()
    rad_2 = models.FloatField()
    teff_2 = models.FloatField()
    massc_2 = models.FloatField()
    radc_2 = models.FloatField()
    menv_2 = models.FloatField()
    renv_2 = models.FloatField()
    epoch_2 = models.FloatField()
    ospin_2 = models.FloatField()
    deltam_2 = models.FloatField()
    rrol_2 = models.FloatField()
    porb = models.FloatField()
    sep = models.FloatField()
    ecc = models.FloatField()
    b_0_1 = models.FloatField()
    b_0_2 = models.FloatField()
    snkick_1 = models.FloatField()
    snkick_2 = models.FloatField()
    vsys_final = models.FloatField()
    sntheta_final = models.FloatField()
    sn_1 = models.FloatField()
    sn_2 = models.FloatField()
    bin_state = models.FloatField()
    merger_type = models.FloatField()
    bin_num = models.FloatField()
    time_id = models.AutoField(primary_key=True)
    # Set the manager
    objects = NodeQuerySet.as_manager()

    # Properties
    @property
    def __str__(self):
        return 'Node: {}'.format(self.time_id)

    @property
    def id(self):
        """ Example Property: Return Node primary key """
        return self.time_id

    # Functions
    def get_id(self, *args, **kwargs):
        """ Example method: Return Node primary key """
        return self.time_id



# Node for health data
class Node2(models.Model):
    file_id = models.IntegerField(db_index=True)
    node_id = models.IntegerField(db_index=True)
    age_yrs = models.FloatField()
    resting_heart_rate = models.FloatField()
    active_heart_rate = models.FloatField()
    blood_pressure = models.FloatField()
    temperature = models.FloatField()
    covid_antibodies = models.FloatField()
    influenza_antibodies = models.FloatField()
    height_in = models.FloatField()
    weight_lbs = models.FloatField()
    bmi = models.FloatField()
    num_teeth = models.FloatField()
    time_id = models.AutoField(primary_key=True)
    # Set the manager
    objects = NodeQuerySet.as_manager()

    # Properties
    @property
    def __str__(self):
        return 'Node2: {}'.format(self.time_id)

    @property
    def id(self):
        """ Example Property: Return Node primary key """
        return self.time_id

    # Functions
    def get_id(self, *args, **kwargs):
        """ Example method: Return Node primary key """
        return self.time_id



# Node for chicken pox data
class Node3(models.Model):
    file_id = models.IntegerField(db_index=True)
    node_id = models.IntegerField(db_index=True)
    Date = models.CharField(max_length=20)
    BUDAPEST = models.FloatField()
    BARANYA = models.FloatField()
    BACS = models.FloatField()
    BEKES = models.FloatField()
    BORSOD = models.FloatField()
    CSONGRAD = models.FloatField()
    FEJER = models.FloatField()
    GYOR = models.FloatField()
    HAJDU = models.FloatField()
    HEVES = models.FloatField()
    JASZ = models.FloatField()
    KOMAROM = models.FloatField()
    NOGRAD = models.FloatField()
    PEST = models.FloatField()
    SOMOGY = models.FloatField()
    SZABOLCS = models.FloatField()
    TOLNA = models.FloatField()
    VAS = models.FloatField()
    VESZPREM = models.FloatField()
    ZALA = models.FloatField()
    time_id = models.AutoField(primary_key=True)
    # Set the manager
    objects = NodeQuerySet.as_manager()

    # Properties
    @property
    def __str__(self):
        return 'Node3: {}'.format(self.time_id)

    @property
    def id(self):
        """ Example Property: Return Node primary key """
        return self.time_id

    # Functions
    def get_id(self, *args, **kwargs):
        """ Example method: Return Node primary key """
        return self.time_id



