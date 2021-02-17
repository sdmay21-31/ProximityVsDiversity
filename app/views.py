from django.shortcuts import render

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

    #Check for request method and respond accordingly
    if request.method == 'GET':
        return render(request, 'nodeForm.html')

    else: #POST Request

        #Create and algorithim form based on recieved data
        form = AlgoRequestForm(request)

        #Assign clean data to attributes
        if form.isValid():
            attribute1 = form.cleaned_data['attribute1']
            attribute2 = form.cleaned_data['attribute2']
            attribute3 = form.cleaned_data['attribute3']

            #Create context from cleaned data
            context = {
                "attribute1": attribute1,
                "attribute2": attribute2,
                "attribute3": attribute3,
            }
            #Send the context to the correct html page
            return render(request, 'nodeForm.html', context)
			

# View for the database choice form
def DatabaseChoiceView(request):

    #Check for request method and respond accordingly
    if request.method == 'GET':
        return render(request, 'databaseChoiceForm.html')

    else: #POST Request

        #Create and algorithim form based on recieved data
        form = AlgoRequestForm(request)

        #Assign clean data to attributes
        if form.isValid():
            choice = form.cleaned_data['choice']

            #Create context from cleaned data
            context = {
                "choice": choice,
            }
            #Send the context to the correct html page
            return render(request, 'databaseChoiceForm.html', context)

