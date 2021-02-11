from djang import forms
from app.models import Node
s
class AlgoRequestForm(forms.Form):
    attribute1 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    attribute2 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    attribute3 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    