from django.core.management.base import BaseCommand, CommandError
import csv
from app.models import Dataset, Simulation

class Command(BaseCommand):
    help = "Adds a new dataset to your application"

    def handle(self, *args, **kwargs):
        with open('datasets/main_table_1.csv') as file:
            reader = csv.DictReader(file)

            next(reader)

            self.headers = reader._fieldnames

            simulation_id = 'node_id'
            attribute_ids = ['mass_1', 'lumin_1', 'rad_1', 'teff_1']

            Dataset.objects.all().delete()
            dataset = Dataset(
                name="testing",
                simulation_attributes=attribute_ids)
            dataset.save()

            TOTAL_SIMULATIONS = 10
            simulation = []
            simulations = []
            current_simulation_id = None

            while len(simulations) < TOTAL_SIMULATIONS:
                line = next(reader, None)
                if line is None:
                    break
                if current_simulation_id is None:
                    current_simulation_id = line[simulation_id]
                    continue
                # If moving on to next simulation
                if current_simulation_id != line[simulation_id]:
                    simulations.append(Simulation(
                        dataset=dataset,
                        simulation_value=current_simulation_id,
                        total_nodes=len(simulation),
                        data=simulation
                    ))
                    current_simulation_id = line[simulation_id]
                    simulation = []
                # Add node to current simulation
                simulation.append([line[col] for col in attribute_ids])

            Simulation.objects.bulk_create(simulations)
            print(Simulation.objects.count())
