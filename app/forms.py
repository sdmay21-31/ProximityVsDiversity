from django import forms
from app.models import Dataset


class SetupDatasetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.filename = kwargs.pop('filename')
        super(SetupDatasetForm, self).__init__(*args, **kwargs)

        self.add_dynamic_fields()

    class Meta:
        model = Dataset
        fields = ['name']

    def add_dynamic_fields(self):
        with open(f'datasets/{ self.filename }') as file:
            header = file.readline()
            headers = header.split(',')

            choices = [(h, h) for h in headers]

            self.fields['simulation_id'] = forms.ChoiceField(
                label="Simulation Id",
                choices=choices,
                help_text="Select One")

            self.fields['attributes'] = forms.MultipleChoiceField(
                label="Attributes",
                choices=choices)