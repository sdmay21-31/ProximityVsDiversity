from django import forms
from app.models import Dataset


class UploadFileForm(forms.Form):
    file = forms.FileField()

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

            self.fields['simulation_ids'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label="Simulation Identifiers",
                help_text="Select the fields that differentiates your different simulations.",
                choices=choices)

            self.fields['attributes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label="Attributes",
                help_text="Select the fields that you would like stored as attributes for your simulations.",
                choices=choices)