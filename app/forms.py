from django import forms
from app.models import Node

class AlgoRequestForm(forms.Form):
    attribute1 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    attribute2 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    attribute3 = forms.ModelMultipleChoiceField(queryset=Node.objects.all())
    
class DatabaseChoiceForm(forms.Form):
    
    givenChoices = (
        ('1', 'Database 1'),
        ('2', 'Database 2'),
        ('3', 'Database 3'),
    )
    
    # For debugging purposes
    #print(givenChoices)
    #print(givenChoices[0])
    #print(givenChoices[1])
    #print(givenChoices[2])
    #print(givenChoices[0][0])
    #print(givenChoices[1][0])
    #print(givenChoices[2][0])
    
    choice = forms.MultipleChoiceField(choices = givenChoices)
    
    text = forms.CharField(label='text', max_length=100)

