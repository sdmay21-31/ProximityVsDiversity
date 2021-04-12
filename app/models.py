from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from app.shims import DatasetShim
from django.core.validators import FileExtensionValidator

class Dataset(DatasetShim, models.Model):
    name = models.CharField(max_length=250, unique=True, help_text="Name of the dataset")
    slug = AutoSlugField(unique=True, populate_from='name')
    file_name = models.CharField(max_length=255, default='main_table_1.csv')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    total_simulations = models.IntegerField(editable=False, default=0)
    total_nodes = models.IntegerField(editable=False, default=0)
    max_simulation_nodes = models.IntegerField(editable=False, default=0)
    min_simulation_nodes = models.IntegerField(editable=False, default=0)

    simulation_fields = models.JSONField(editable=False, default=dict)
    attributes = models.JSONField(editable=False)
    """Structure
    ['attr1', 'attr2', 'attr3']
    """

    class Meta:
        db_table = "dataset"

class Simulation(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, editable=False)
    total_nodes = models.IntegerField(editable=False)
    
    data = models.JSONField(editable=False)
    """Structure
    [
        ['attr1', 'attr2', ...],
        ['attr1', 'attr2', 'attr3']
    ]
    """

    class Meta:
        db_table = "simulation"