from django import forms
from app.models import Dataset


class SetupDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'created_by_name', 'created_by_email']