from django.contrib import admin
from app.models import Dataset

# Register your models here.

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ('total_simulations', )
