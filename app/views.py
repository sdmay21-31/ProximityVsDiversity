from django.shortcuts import render
from django.views import FormView
from app.algos import example_algo
from app.forms import AlgoRequestForm

# Create your views here.
def index(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    return render(request, 'index.html', context)

#View for the algorithim request form
def AlgoRequestView(request):

    #Create and algorithim form based on recieved data
    form = AlgoRequestForm(request)

    #Assign clean data to attributes
    if form.isValid():
        attribute1 = form.cleaned_data['attribute1']
        attribute2 = form.cleaned_data['attribute2']
        attribute3 = form.cleaned_data['attribute3']

            #Create context from cleaned data (NOTE: Currently placeholder and not correct)
            contex = {
                [attribute1,attribute2,attribute3]: example_algo()[:10]
            }
        return render(request, 'index.html', context)
    else
        #Place holder error return
        return render(request, 'index.html', "ERROR MESSAGE")
