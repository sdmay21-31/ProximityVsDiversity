from djang import forms

class AlgoRequestForm(forms.Form):
    name = forms.CharField(label="Algo Request Form")
    algo = null
        
    