from django import forms
from app.models import Dataset, DataFile


class SetupDatasetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.datafile = DataFile.objects.get(slug=kwargs.pop('file_slug'))
        super(SetupDatasetForm, self).__init__(*args, **kwargs)

        self.add_dynamic_fields()

    class Meta:
        model = Dataset
        fields = ['name', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.attributes = self.cleaned_data['attributes']
        instance.simulation_fields = self.cleaned_data['simulation_fields']
        instance.datafile = self.datafile
        instance.set_created()
        if commit:
            instance.save()
        return instance

    def add_dynamic_fields(self):
        with open(self.datafile.file.path) as file:
            header = file.readline()
            headers = header.split(',')

            choices = [(h, h) for h in headers]

            self.fields['simulation_fields'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label="Simulation Fields",
                help_text="Select the fields that differentiates your different simulations.",
                choices=choices)

            self.fields['attributes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label="Attributes",
                help_text="Select the fields that you would like stored as attributes for your simulations.",
                choices=choices)