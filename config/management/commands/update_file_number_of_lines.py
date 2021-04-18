from django.core.management.base import BaseCommand
from app.models import DataFile


class Command(BaseCommand):
    help = "Update datafiles"

    def handle(self, *args, **kwargs):
        for datafile in DataFile.objects.all():
            with open(datafile.file.path) as f:
                datafile.number_of_lines = sum(1 for line in f)
                datafile.save()
