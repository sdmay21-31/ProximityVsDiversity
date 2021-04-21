from django.core.management.base import BaseCommand
from app.models import Node
from django.db.models import Count

class Command(BaseCommand):
    help = "Update datafiles"

    def handle(self, *args, **kwargs):
        for n in Node.objects.values('dataset', 'simulation').annotate(total_nodes=Count('simulation')):
            Node.objects.filter(dataset_id=n['dataset']).filter(simulation=n['simulation']).update(simulation_total_nodes=n['total_nodes'])
