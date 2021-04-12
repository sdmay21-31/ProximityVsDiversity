from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from app.shims import DatasetShim
from django.urls import reverse_lazy
from django.core.validators import FileExtensionValidator


class Dataset(DatasetShim, models.Model):
    class Statuses(models.IntegerChoices):
        CREATED = 0, 'Created'
        SEEDING = 1, 'Seeding'
        COMPLETED = 2, 'Completed'
        ERROR = 3, 'Error'
        LEGACY = 4, 'Legacy'

    name = models.CharField(max_length=250, unique=True,
                            help_text="Name of the dataset")
    description = models.CharField(max_length=250, default='')
    slug = AutoSlugField(unique=True, populate_from='name')
    file_name = models.CharField(max_length=255, default='main_table_1.csv')
    status = models.IntegerField(
        choices=Statuses.choices, default=Statuses.LEGACY)

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

    def get_absolute_url(self):
        return reverse_lazy('edit', args=(self.slug, ))

    def set_created(self):
        self.status = Dataset.Statuses.CREATED

    def set_seeding(self):
        self.status = Dataset.Statuses.SEEDING

    def set_completed(self):
        self.status = Dataset.Statuses.COMPLETED

    def set_error(self):
        self.status = Dataset.Statuses.ERROR

    def is_processable(self):
        return self.status == Dataset.Statuses.COMPLETED or self.status == Dataset.Statuses.LEGACY


class Simulation(models.Model):
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, editable=False)
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
