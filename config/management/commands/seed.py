from django.core.management.base import BaseCommand, CommandError
from app import seed
from app.models import Node

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--full', action='store_true', help='Seed the entire database (takes a minute)')

    def handle(self, *args, **kwargs):
        full = kwargs.get('full', False) or kwargs.get('f')
        # Delete table
        Node.objects.all().delete()

        if full:
            print('Seeding full database')
            seed.run(True)
        else:
            print('Seeding 10000 nodes')
            seed.run()
