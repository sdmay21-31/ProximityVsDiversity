from django.shortcuts import render, redirect

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



# Database names defined for database choice page
DATABASE_NAMES = (
    'DatabaseOne',
    'DatabaseTwo',
    'DatabaseThree',
)

# View for the database choice form
def DatabaseChoiceView(request):
    
    #Check for request method and respond accordingly
    if request.method == 'GET':
        
        form = DatabaseChoiceForm()
        
        #Create context from cleaned data
        context = {
            'form': form,
        }
        
        return render(request, 'databaseChoiceForm.html', context)
        
    else: #POST Request
        
        #Create a database choice form based on recieved data
        form = DatabaseChoiceForm(request.POST)
        
        #Assign clean data to attributes
        if form.is_valid():
            
            choice = form.cleaned_data['choice']
            choiceIndex = int(choice) - 1
            databaseName = DATABASE_NAMES[choiceIndex]
            
            #Send the context to the correct html page
            return redirect(databaseName)



# View for the database one page
def DatabaseOneView(request):
    
    databasePage = "DatabaseOnePage.html"
    
    return render(request, databasePage)

# View for the database two page
def DatabaseTwoView(request):
    
    databasePage = "DatabaseTwoPage.html"
    
    return render(request, databasePage)

# View for the database three page
def DatabaseThreeView(request):
    
    databasePage = "DatabaseThreePage.html"
    
    return render(request, databasePage)
