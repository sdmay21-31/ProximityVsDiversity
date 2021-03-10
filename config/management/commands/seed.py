from django.core.management.base import BaseCommand, CommandError
from app import seed
from app.models import Node, Node2, Node3
from app.seed import nodeDictionary


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--full', action='store_true',
                            help='Seed the entire database. Seeds nodes in 10,000 node chunks, and takes about an hour.')
        
        parser.add_argument('-d', '--database', dest='database',
                            action='store', default='main_table_1.csv',
                            help='Specify the database to seed.')
        
        # For debugging purposes
        # parser.parse_args(['--database', 'main_table_2.csv'])
        
        nodes2 = Node2.objects.all()
        print(nodes2.count())
        #print(str)
        #nodesStr = nodes1.__str__
        #print(nodesStr)
        
        
        



    def handle(self, *args, **kwargs):
        full = kwargs.get('full', False) or kwargs.get('f')
        database = kwargs.get('database', False) or kwargs.get('d')
        
        # Delete all rows
        #Node.objects.all().delete()
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        print('Database: ' + database)
        
        if full:
            print('Seeding full database')
            print(
                'You can stop at any point with ctrl+c, and the nodes will be saved. This process will take about an hour to run to completion and it is insteaed recommended to run a direct sql query to import the data.')
            seed.run(database, True)
        else:
            print('Seeding 10000 nodes')
            seed.run(database)
