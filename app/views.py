from django.shortcuts import render, redirect
import json
from django.http import JsonResponse


from app.algos import example_algo
from app.forms import AlgoRequestForm, DatabaseChoiceForm
from app.algos import example_algo, gabe


# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'index.html')

def dummyDB(request, *args, **kwargs):
    return JsonResponse({'dbs': ['hello_world', 'yay_me', 'im_london_tipton']})

def dummyPost(request):
    print(request.body)
    return JsonResponse({'test': 'i dont understand python'})
    #the dummyPost above prints the request body to the command prompt
    
def dummyAttr(request, db):
    dbToAttrs = {
        "hello_world":["goodbye", "hello", "world", "earth"],
        "tipton":["maddie", "moseby", "hotel", "ship"],
        "yay_me":["london", "podcast"]
    }
    return JsonResponse({'attrs': dbToAttrs[db]})

def indexQS(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    gabe.run()
    return render(request, 'index.html', context)

#Alright, this is a start to JSON inputs from the possible frontend stuff
def processAttr(request):
    
    #fail on non post request
    if request.method != "POST":
        return "ERROR WITH REQUEST"

    #This is where the form input for json is created for the form
    #Maybe? do we need a form if JSON exists?

    #grab json attrs
    proxAttr = json.loads(request.data.get("proxAttrs"))
    divAttrs = json.loads(request.data.get("divAttrs"))

    #Send data to db/algo

    #This part is semi-tricky on how to implement, it depends upon algorithim input and should be dynamic
    #lists are a good start to split attr/values and send them



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
