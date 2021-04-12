import os
from celery import shared_task
import csv
from app.models import Dataset, Simulation
from django.db.models import Sum, Max, Min
from django.conf import settings


def get_simulations(reader, dataset, chunk_size=500):
    simulation = []
    simulations = []
    line = next(reader)
    current_simulation_values = []
    current_file_id = line['file_id']

    def is_new_simulation():
        for index, v in enumerate(current_simulation_values):
            if v != line[dataset.simulation_fields[index]]:
                return True
        return False

    def add_simulation():
        simulations.append(Simulation(
            dataset=dataset,
            total_nodes=len(simulation),
            data=simulation
        ))

    current_simulation_values = [
        line[attr] for attr in dataset.simulation_fields
    ]

    while True:
        # Return simulations chunk
        if len(simulations) >= chunk_size:
            yield simulations
            simulations = []
        # Finished
        if line is None:
            if len(simulation) > 0:
                add_simulation()
            if len(simulations) > 0:
                yield simulations
            return None

        # If moving on to next simulation
        if is_new_simulation():
            add_simulation()
            current_simulation_values = [
                line[attr] for attr in dataset.simulation_fields
            ]
            simulation = []

        simulation.append([line[col] for col in dataset.attributes])
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
        with open(os.path.join(settings.BASE_DIR, 'datasets', dataset.file_name)) as file:
            reader = csv.DictReader(file)

            headers = reader.fieldnames

            for simulations in get_simulations(reader, dataset):
                Simulation.objects.bulk_create(simulations)

            aggs = dataset.simulation_set.aggregate(
                Sum('total_nodes'), Max('total_nodes'), Min('total_nodes'))

            dataset.total_simulations = dataset.simulation_set.count()
            dataset.total_nodes = aggs['total_nodes__sum']
            dataset.max_simulation_nodes = aggs['total_nodes__max']
            dataset.min_simulation_nodes = aggs['total_nodes__min']
            dataset.set_completed()
            dataset.save()
    except Exception as e:
        dataset.set_error()
        raise e
