from django.shortcuts import render

from app.algos import example_algo
from app.forms import AlgoRequestForm, DatabaseChoiceForm

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
        
        # For debugging purposes
        print("GET request...")
        
        return render(request, 'databaseChoiceForm.html')

    else: #POST Request
        
        # For debugging purposes
        print("POST request...")
        
        #Create a database choice form based on recieved data
        form = DatabaseChoiceForm(request)
        
        # For debugging purposes
        print("Is the form valid?")
        
        #Assign clean data to attributes
        if form.isValid():
            choice = form.cleaned_data['choice']
            text = form.cleaned_data['text']
            
            #Create context from cleaned data
            context = {
                'choice': choice,
                'text': text,
            }
            #context = {
            #    'form': form,
            #}
            
            # For debugging purposes
            print("Yes...")
            print("View Data: ")
            print(choice)
            print(choice[0])
            print(choice[1])
            print(choice[2])
            print(choice[0][0])
            print(choice[1][0])
            print(choice[2][0])
            
            #Send the context to the correct html page
            return render(request, 'databaseChoiceForm.html', context)

