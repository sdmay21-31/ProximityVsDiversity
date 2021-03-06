from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.forms import AlgoRequestForm, DatabaseChoiceForm
from app.algos import example_algo, gabe

from app.models import Node
from collections import Counter

app_config = apps.get_app_config('app')
# can't use app_models because it can only be read once
# app_models = app_config.get_models()

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'index.html')

# def dummyDB(request, *args, **kwargs):
#     return JsonResponse({'dbs': ['hello_world', 'yay_me', 'im_london_tipton']})
    
# def dummyAttr(request, db):
#     dbToAttrs = {
#         "hello_world":["goodbye", "hello", "world", "earth"],
#         "tipton":["maddie", "moseby", "hotel", "ship"],
#         "yay_me":["london", "podcast"]
#     }
#     return JsonResponse({'attrs': dbToAttrs[db]})

def getDBs(request, *args, **kwargs):
    return JsonResponse({'dbs': [m.__name__ for m in app_config.get_models()]})

def getAttrs(request, db):
    attrs = [f.name for f in app_config.get_model(db)._meta.fields]
    seen = set()
    filtered_attrs = [a[:-2] for a in attrs if
        (a[-2:] in ['_1', '_2'] and (a[:-2] in seen or seen.add(a[:-2])))
    ]
    return JsonResponse({'attrs': [f for f in filtered_attrs if '{}_1'.format(f) in attrs and '{}_2'.format(f) in attrs]})

def dummyPost(request):
    print(request.body)
    return JsonResponse({'test': 'i dont understand python'})

def indexQS(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    gabe.run()
    return render(request, 'index.html', context)

#View for the algorithm request form
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
            return render(request, 'nodeForm.html', context)
