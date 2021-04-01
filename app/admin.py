from django.contrib import admin
from app.models import Node, Simulation, Dataset

# Register your models here.
admin.site.register(Node)
admin.site.register(Simulation)
admin.site.register(Dataset)