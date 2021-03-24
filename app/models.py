from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_email = models.EmailField()
    created_by_name = models.CharField(max_length=250)

    total_simulations = models.IntegerField()
    total_nodes = models.IntegerField()
    max_simulation_nodes = models.IntegerField()
    min_simulation_nodes = models.IntegerField()
    simulation_id = models.CharField(max_length=50)


class Simulation(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    simulation_value = models.CharField()
    total_nodes = models.IntegerField()
    attributes = models.JSONField()
    """Structure
    {
        'attr_key': {
            'name': string,
            'data_index': int
        }
    }
    """
    data = models.JSONField()
    """Structure
    [
        ['attr1', 'attr2', ...],
        ['attr1', 'attr2', 'attr3']
    ]
    """


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
