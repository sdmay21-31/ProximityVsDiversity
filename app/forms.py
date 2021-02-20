from django import forms
from app.models import Node

NODE_ATTR_CHOICES = (
    ("1", "tphys"),
    ("2", "kstar_1"),
    ("3", "mass0_1"),
    ("4", "mass_1"),
    ("5", "lumin_1"),
    ("6", "rad_1"),
    ("7", "teff_1"),
    ("8", "massc_1"),
    ("9", "radc_1"),
    ("10", "menv_1"),
    ("11", "renv_1"),
    ("12", "epoch_1"),
    ("13", "opsin_1"),
    ("14", "deltam_1"),
    ("15", "rrol_1"),
    ("16", "kstar_2"),
    ("17", "mass0_2"),
    ("18", "mass_2"),
    ("19", "lumin_2"),
    ("20", "rad_2"),
    ("21", "teff_2"),
    ("22", "massc_2"),
    ("23", "radc_2"),
    ("24", "menv_2"),
    ("25", "renv_2"),
    ("26", "epoch_2"),
    ("27", "opsin_2"),
    ("28", "deltam_2"),
    ("29", "rrol_12"),
    ("30", "porb"),
    ("31", "sec"),
    ("32", "ecc"),
)

class AlgoRequestForm(forms.Form):

    #List and select wanted attr
    attribute1 = forms.ChoiceField(choices=NODE_ATTR_CHOICES)
    attribute2 = forms.ChoiceField(choices=NODE_ATTR_CHOICES)
    attribute3 = forms.ChoiceField(choices=NODE_ATTR_CHOICES)

    attribute1Value = forms.FloatField()
    attribute2Value = forms.FloatField()
    attribute3Value = forms.FloatField()
    
class DatabaseChoiceForm(forms.Form):
    
    givenChoices = (
        ('1', 'Database 1'),
        ('2', 'Database 2'),
        ('3', 'Database 3'),
    )
    
    choice = forms.ChoiceField(choices = givenChoices)
    

