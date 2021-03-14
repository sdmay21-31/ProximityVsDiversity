import csv

from app.seed import nodeDictionary

def run(file_name='main_table_1.csv'):
        # Get the node type
        node_type = nodeDictionary[file_name]

        count = node_type.objects.count()
        exist = node_type.objects.exists()
        allElements = node_type.objects.all()
        print("Count: " + str(count))
        print("Exists: " + str(exist))
        print("All elements: " + str(allElements))