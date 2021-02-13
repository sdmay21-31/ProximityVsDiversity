from django import forms
from app.models import Node

class AlgoRequestForm(forms.Form):
    attribute1 = forms.ChoiceField(widget=forms.Select, choices=Node.objects.all())
    attribute2 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    attribute3 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    