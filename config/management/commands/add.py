from django.core.management.base import BaseCommand, CommandError
import csv

class Command(BaseCommand):
    missing_args_message = 'Please add the file you would like to add'
    help = "Adds a new dataset to your application"

    def add_arguments(self, parser):
        parser.add_argument('file', help='Select the file to import.')

    def handle(self, *args, **kwargs):
        with open(kwargs.get('file')) as file:
            reader = csv.DictReader(file)

            next(reader)

            self.headers = reader._fieldnames
            self.list_headers()

            simulation_id = self.get_user_input_col(
                'Enter the Simulation Identifier: ')

            attribute_ids = self.get_user_input_cols(
                'Enter attribute identifiers you would like to use seperated by commas:\n')

            line = next(reader)
            line = next(reader)

            current_simulation = line[simulation_id]
            next_simulation = current_simulation
            count = 0

            while current_simulation == next_simulation:
                line = next(reader)
                next_simulation = line[simulation_id]
                count += 1

            print(current_simulation, next_simulation, count)

    def list_headers(self, list_display=True):
        print("Available identifiers")
        print("====================")
        for header in self.headers:
            print(header)

    def validate_header(self, header):
        if not header in self.headers:
            raise ValueError

    def get_user_input_col(self, question):
        value = input(question)
        self.validate_header(value)
        return value

    def get_user_input_cols(self, question):
        value = input(question)
        values = [v.strip() for v in value.split(',')]
        for value in values:
            self.validate_header(value)
        return values

