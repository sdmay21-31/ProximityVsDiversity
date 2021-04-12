from django.contrib import admin
from app.models import Simulation, Dataset

# Register your models here.

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ('total_simulations', )

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_nodes')