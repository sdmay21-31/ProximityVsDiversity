import csv

from app.models import Node

TOTAL_NODES = 10355968


def get_chunks(csv_reader, chunk_size):
    nodes = []
    count = 0
    while True:
        n = next(csv_reader)
        # EOF
        if not n:
            break
        # Building Nodes
        if count < chunk_size:
            nodes.append(Node(**dict(n)))
            count += 1
        # Return nodes
        else:
            yield nodes
            nodes = []
            count = 0


def run(full_seed=False, chunk_size=10000, print_status=True):
    with open('datasets/main_table_1.csv') as f:
        csv_reader = csv.DictReader(f)
        # Read In Headers
        next(csv_reader)
        # Change id to node_id
        csv_reader._fieldnames[1] = 'node_id'
        # Our nodes
        chunk_count = 0
        # Read File
        for chunk in get_chunks(csv_reader, chunk_size):
            # Create Node objects
            Node.objects.bulk_create(chunk)
            chunk_count += 1
            if print_status:
                print('Nodes: {}/{}'.format(chunk_count * chunk_size, TOTAL_NODES))
            # Exit if not seeding full database
            if not full_seed:
                break
