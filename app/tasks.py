from celery import shared_task
import csv
from app.models import Dataset, Node
from django.db.models import Sum, Max, Min


def relativise(value, mmax, mmin):
    try:
        return (value - mmin) / (mmax - mmin)
    except ZeroDivisionError:
        return 0


def get_nodes(reader, dataset, chunk_size=1000):
    simulation_number = 0
    number_of_attributes = len(dataset.attributes)
    simulation = []
    nodes = []
    line = next(reader)
    current_simulation_values = []

    def is_new_simulation():
        nonlocal current_simulation_values
        for index, v in enumerate(current_simulation_values):
            if v != line[dataset.simulation_fields[index]]:
                return True
        return False

    def process_simulation():
        nonlocal simulation_number
        simulation_number += 1
        maxs = [0 for n in range(number_of_attributes)]
        mins = [float('inf') for n in range(number_of_attributes)]
        total_nodes = len(simulation)

        # Find the min and max
        for node in simulation:
            for index in range(number_of_attributes):
                if node[index] > maxs[index]:
                    maxs[index] = node[index]
                if node[index] < mins[index]:
                    mins[index] = node[index]

        for index, n in enumerate(simulation):
            relativised_data = [
                relativise(n[index], maxs[index], mins[index])
                for index in range(number_of_attributes)
            ]
            node = Node(
                dataset=dataset,
                simulation=simulation_number,
                simulation_index=index,
                simulation_total_nodes=total_nodes,
                data=n,
                relativised_data=relativised_data
            )
            nodes.append(node)

    current_simulation_values = [
        line[attr] for attr in dataset.simulation_fields
    ]

    while True:
        # Finished
        if line is None:
            if len(nodes) > 0:
                process_simulation()
            if len(nodes) > 0:
                yield nodes
            return None

        # If moving on to next simulation
        if is_new_simulation():
            process_simulation()
            current_simulation_values = [
                line[attr] for attr in dataset.simulation_fields
            ]
            simulation = []
            # Return nodes chunk
            if len(nodes) >= chunk_size:
                yield nodes
                nodes = []

        simulation.append([float(line[col]) for col in dataset.attributes])
        # Increment line
        try:
            line = next(reader)
        except StopIteration:
            line = None


@shared_task
def seed_dataset(dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    try:
        dataset.set_seeding()
        dataset.save()
        with open(dataset.datafile.file.path) as file:
            reader = csv.DictReader(file)

            for nodes in get_nodes(reader, dataset):
                n = Node.objects.bulk_create(nodes)
                dataset.number_of_nodes_added += len(n)
                dataset.save()

            aggs = dataset.node_set.aggregate(
                Max('simulation')
            )
            dataset.total_nodes = dataset.node_set.count()
            dataset.total_simulations = aggs['simulation__max']
            dataset.set_completed()
            dataset.save()
    except Exception as e:
        dataset.set_error()
        dataset.save()
        raise e
