from django.core.management.base import BaseCommand, CommandError
from app import seed
from app.models import Node


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--full', action='store_true',
                            help='Seed the entire database. Seeds nodes in 10,000 node chunks, and takes about an hour.')

    def handle(self, *args, **kwargs):
        full = kwargs.get('full', False) or kwargs.get('f')
        # Delete all rows
        Node.objects.all().delete()

        if full:
            print('Seeding full database')
            print(
                'You can stop at any point with ctrl+c, and the nodes will be saved. This process will take about an hour to run to completion and it is insteaed recommended to run a direct sql query to import the data.')
            seed.run(True)
        else:
            print('Seeding 10000 nodes')
            seed.run()
