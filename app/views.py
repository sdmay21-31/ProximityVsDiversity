from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.forms import AlgoRequestForm, DatabaseChoiceForm
from app.algos import run as run_algo

from app.databases import get_database_attributes, get_databases

from app.models import Node
from collections import Counter


# Create your views here.
def guide(request):
    return render(request, 'user_documentation.html')
    
def index(request, *args, **kwargs):
    """Default index page"""
    return render(request, 'index.html')

def databases(request, *args, **kwargs):
    """Return list of databases"""
    return JsonResponse({'dbs': get_databases()})

def attributes(request, database):
    """Return attributes from model and strip _1 and _2"""
    return JsonResponse({'attrs': get_database_attributes(database)})

def process(request):
    """Return the algorithm function"""
    # TODO: validate incoming data
    # TODO: Use database map to get attributes
    (chart, data) = run_algo(
        method='kmeans',
        time_frame=1,
        proximity=[{'mass_1': 10, 'lumin_1': 20, 'rad_1': 20}],
        diversity=[])
    return JsonResponse({
        'chart': chart,
        'data': data
        })
