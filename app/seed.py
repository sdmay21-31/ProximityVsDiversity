import csv

from app.models import Node, Node2, Node3

TOTAL_NODES = 10355968


def get_chunks(csv_reader, chunk_size, node_type):
    nodes = []
    count = 1
    while True:
        try:
            n = next(csv_reader)
        except StopIteration:
            # EOF
            yield nodes
            break

        # For debugging purposes
        if count < 6 or count > 9995:
            print(n)

        # Building Nodes
        nodes.append(node_type(**dict(n)))
        if count < chunk_size:
            count += 1
        # Return nodes
        else:
            yield nodes
            nodes = []
            count = 1


def run(file_name='main_table_1.csv', full_seed=False, chunk_size=10000, print_status=True):
    with open('datasets/' + file_name) as f:
        csv_reader = csv.DictReader(f)
        # Our nodes
        chunk_count = 0
        
        # Get the node type
        node_type = nodeDictionary[file_name]
        
        # Read File
        for chunk in get_chunks(csv_reader, chunk_size, node_type): # Generator fails...
            # Create Node objects
            #Node.objects.bulk_create(chunk)
            node_type.objects.bulk_create(chunk)
            chunk_count += 1
            if print_status:
                print('Nodes: {}/{}'.format(chunk_count * chunk_size, TOTAL_NODES))
            # Exit if not seeding full database
            if not full_seed:
                break



# Node dictionary
nodeDictionary = {
    "main_table_1.csv": Node,
    "main_table_2.csv": Node2,
    "hungary_chickenpox.csv": Node3
}

