from django.contrib import admin
from app.models import Node, Simulation, Dataset

# Register your models here.
admin.site.register(Node)
admin.site.register(Dataset)

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_nodes')