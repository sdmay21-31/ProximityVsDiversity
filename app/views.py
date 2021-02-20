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
    if request.method == "GET":
        return render(request, 'nodeForm.html',{'form': AlgoRequestForm()})

    else: #POST Request

        #Create and algorithim form based on recieved data
        form = AlgoRequestForm(request)

        #Assign clean data to attributes
        if form.is_valid():
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
    
    databasePage = "DatabaseOnePage.html"
    
    #Check for request method and respond accordingly
    if request.method == 'GET':
        
        # For debugging purposes
        print("GET request...")
        
        form = DatabaseChoiceForm()
        
        return render(request, 'databaseChoiceForm.html', {'form': form})

    else: #POST Request
        
        # For debugging purposes
        print("POST request...")
        
        #Create a database choice form based on recieved data
        form = DatabaseChoiceForm(request.POST)
        
        #Assign clean data to attributes
        if form.is_valid():
            
            databaseName = "DatabaseOne"
            
            choice = form.cleaned_data['choice']
            
            if (choice == 2):
                databaseName = "DatabaseTwo"
            
            if (choice == 3):
                databaseName = "DatabaseThree"
            
            #Create context from cleaned data
            context = {
                'form': form,
				'databaseName': databaseName,
            }
            
            databasePage = databaseName + "Page.html"
            
            #Send the context to the correct html page
            return render(request, 'databaseChoiceForm.html', context)

# View for the database page that was chosen
def DatabasePageView(request):
    
    databasePage = "DatabaseOnePage.html"
    
    #Check for request method and respond accordingly
    if request.method == 'GET':
        
        form = DatabaseChoiceForm()
        
        return render(request, databasePage)

    else: #POST Request
        
        #Create a database choice form based on recieved data
        form = DatabaseChoiceForm(request.POST)
        
        #Assign clean data to attributes
        if form.is_valid():
            
            databaseName = "DatabaseOne"
            
            choice = form.cleaned_data['choice']
            
            if (choice == 2):
                databaseName = "DatabaseTwo"
            
            if (choice == 3):
                databaseName = "DatabaseThree"
            
            #Create context from cleaned data
            context = {
                'choice': choice,
				'databaseName': databaseName,
            }
            
            databasePage = databaseName + "Page.html"
            
            #Send the context to the correct html page
            return render(request, databasePage, context)

