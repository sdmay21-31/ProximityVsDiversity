from django.db import models
from django.conf import settings
from app.shims import DatasetShim

class Dataset(DatasetShim, models.Model):
    name = models.CharField(max_length=250, unique=True, help_text="Name of the dataset")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    total_simulations = models.IntegerField(default=0)
    total_nodes = models.IntegerField(default=0)
    max_simulation_nodes = models.IntegerField(default=0)
    min_simulation_nodes = models.IntegerField(default=0)
    simulation_attributes = models.JSONField()
    """Structure
    ['attr1', 'attr2', 'attr3']
    """

    class Meta:
        db_table = "dataset"

class Simulation(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    total_nodes = models.IntegerField()
    
    data = models.JSONField()
    """Structure
    [
        ['attr1', 'attr2', ...],
        ['attr1', 'attr2', 'attr3']
    ]
    """

    class Meta:
        db_table = "simulation"

class Node(models.Model):
    pass