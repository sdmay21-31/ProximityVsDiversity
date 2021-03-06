from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from app.shims import DatasetShim
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse_lazy
from django.core.validators import FileExtensionValidator
from django.db.models import F, Count, Max, ExpressionWrapper, PositiveIntegerField, IntegerField
from django.db.models.functions import Cast


class DataFile(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(unique=True, populate_from="name")
    file = models.FileField(
        upload_to="datasets",
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xls'])])
    number_of_lines = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dataset_file"


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
    datafile = models.ForeignKey(
        DataFile, on_delete=models.SET_NULL,
        null=True, blank=True)
    file_name = models.CharField(max_length=255, default='main_table_1.csv')
    status = models.PositiveIntegerField(
        choices=Statuses.choices, default=Statuses.LEGACY)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    total_simulations = models.PositiveIntegerField(editable=False, default=0)
    total_nodes = models.PositiveIntegerField(editable=False, default=0)

    number_of_nodes_added = models.PositiveIntegerField(default=0)

    simulation_fields = models.JSONField(editable=False, default=dict)
    attributes = models.JSONField(editable=False)
    """Structure
    ['attr1', 'attr2', 'attr3']
    """

    class Meta:
        db_table = "dataset"

    def __str__(self):
        return self.name

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
        return self.status == Dataset.Statuses.COMPLETED or \
            self.status == Dataset.Statuses.LEGACY

    def max_simulation_nodes(self):
        return self.node_set.aggregate(
            Max('simulation_total_nodes'))['simulation_total_nodes__max']


class NodeQuerySet(models.QuerySet):
    def filter_timeframe(self, time_percentage):
        return self.filter(simulation_index=Cast(
                F('simulation_total_nodes') * time_percentage,
                output_field=PositiveIntegerField()))


class Node(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, editable=False)
    simulation = models.PositiveIntegerField(db_index=True)
    simulation_index = models.PositiveIntegerField(db_index=True)
    simulation_total_nodes = models.PositiveIntegerField(db_index=True, default=0)
    data = ArrayField(models.FloatField())
    relativised_data = ArrayField(models.FloatField())

    objects = NodeQuerySet.as_manager()

    class Meta:
        db_table = "node"
