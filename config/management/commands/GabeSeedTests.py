from django.core.management.base import BaseCommand, CommandError
from app import GabeSeedTests


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        
        parser.add_argument('-d', '--database', dest='database',
                            action='store', default='main_table_1.csv',
                            help='Specify the database to seed.')

    def handle(self, *args, **kwargs):
        database = kwargs.get('database', False) or kwargs.get('d')

        if not database:
            GabeSeedTests.run()
        else:
            GabeSeedTests.run(database)
