from django.shortcuts import render

from app.algos import example_algo
from app.forms import AlgoRequestForm

# Create your views here.
def index(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    return render(request, 'index.html', context)

#Defined array for node names
NODE_ATTR_CHOICES = (
     'tphys',
    'kstar_1',
    'mass0_1',
    'mass_1',
    'lumin_1',
    'rad_1',
    'teff_1',
    'massc_1',
    'radc_1',
    'menv_1',
    'renv_1',
    'epoch_1',
    'opsin_1',
    'deltam_1',
    'rrol_1',
    'kstar_2',
    'mass0_2',
    'mass_2',
    'lumin_2',
    'rad_2',
    'teff_2',
    'massc_2',
    'radc_2',
    'menv_2',
    'renv_2',
    'epoch_2',
    'opsin_2',
    'deltam_2',
    'rrol_12',
    'porb',
    'sec',
    'ecc'
)

#View for the algorithim request form
def AlgoRequestView(request):

    #Check for request method and respond accordingly
    if request.method == "GET":
        return render(request, 'nodeForm.html',{'form': AlgoRequestForm()})

    else: #POST Request

        #Create and algorithim form based on recieved data
        form = AlgoRequestForm(request.POST)

        #Assign clean data to attributes
        if form.is_valid():
            #Grab clean attr
            attribute1 = NODE_ATTR_CHOICES[int(form.cleaned_data['attribute1'])-1]
            attribute2 = NODE_ATTR_CHOICES[int(form.cleaned_data['attribute2'])-1]
            attribute3 = NODE_ATTR_CHOICES[int(form.cleaned_data['attribute3'])-1]

            #Grab cleaned values
            attribute1Value = form.cleaned_data['attribute1Value']
            attribute2Value = form.cleaned_data['attribute2Value']
            attribute3Value = form.cleaned_data['attribute3Value']

            #Create context from cleaned data
            context = {
                "attribute1": attribute1,
                "attribute2": attribute2,
                "attribute3": attribute3,
                "attribute1Value": attribute1Value,
                "attribute2Value": attribute2Value,
                "attribute3Value": attribute3Value
            }
            #Send the context to the correct html page
            return render(request, 'nodeView.html', context)
