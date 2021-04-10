from django.core.management.base import BaseCommand, CommandError
import csv
from app.models import Dataset, Simulation

class Command(BaseCommand):
    help = "Adds a new dataset to your application"

    def handle(self, *args, **kwargs):
        with open('datasets/main_table_1.csv') as file:
            reader = csv.DictReader(file)

            self.headers = reader._fieldnames
            if 'node_id' in self.headers:
                self.simulation_id = 'node_id'
            else:
                self.simulation_id = 'id'
            self.attribute_ids = ['mass_1', 'lumin_1', 'rad_1', 'teff_1']

            Dataset.objects.all().delete()
            self.dataset = Dataset(
                name="Astro Physics",
                attributes=self.attribute_ids)
            self.dataset.save()

            for simulations in self.get_simulations(reader):
                Simulation.objects.bulk_create(simulations)

            print(Simulation.objects.count())

    def get_simulations(self, reader, chunk_size=500):
        def get_id(line):
            return line['node_id'].zfill(6) + line['file_id'].zfill(4)
        simulation = []
        simulations = []
        line = next(reader)
        current_simulation_id = get_id(line)
        current_file_id = line['file_id']

        while True:
            # Return simulations chunk
            if len(simulations) >= chunk_size:
                yield simulations
                simulations = []
            # Finished
            if line is None:
                if len(simulations) > 0:
                    yield simulations
                return None

            # If moving on to next simulation
            line_simulation_id = get_id(line)
            if current_simulation_id != line_simulation_id:
                if line['file_id'] != current_file_id:
                    current_file_id = line['file_id']
                    print(f'File Finished: {current_file_id}')
                simulations.append(Simulation(
                    id=line_simulation_id,
                    dataset=self.dataset,
                    total_nodes=len(simulation),
                    data=simulation
                ))
                current_simulation_id = line_simulation_id
                simulation = []

            simulation.append([line[col] for col in self.attribute_ids])
            # Increment line
            try:
                line = next(reader)
            except StopIteration:
                line = None
