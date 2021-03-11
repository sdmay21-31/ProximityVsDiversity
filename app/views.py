from django.apps import apps
from django.shortcuts import render, redirect
import json
from jsonschema import validate
from django.http import JsonResponse

from app.forms import AlgoRequestForm, DatabaseChoiceForm
from app.algos import run as run_algo

from app.databases import get_database_attributes, get_databases

from app.models import Node
from collections import Counter


# Create your views here.
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
    
    #Json Schema to validate data
    expectedJson = {
        "type": "object",
        "properties": {
            'db': {'type' : "string"},
            'time': {'type' : "number"},
            'cluster': {'type' : "number"},
            'proxAttrs': [
                {
                'name': {'type' : "string"},
                'weight': {'type' : "number"}
                },
                {
                'name': {'type' : "string"},
                'weight': {'type' : "number"}
                }
            ],
            'divAttrs': [
                {
                    'name': {'type' : "string"},
                    'weight': {'type' : "number"}
                },
                {
                    'name': {'type' : "string"},
                    'weight': {'type' : "number"}
                }
            ],
        },
    }
    
    data = json.loads(request.body)

    #validate incoming data
    validate(instance=data, schema=expectedJson)

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