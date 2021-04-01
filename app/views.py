from os import walk

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.forms import SetupDatasetForm
from app.algos import run as run_algo

from app.databases import get_database_attributes, get_databases

from app.models import Node, Dataset
from collections import Counter
from app.matplot import plot_to_uri


# Create your views here.
def guide(request):
    return render(request, 'user_documentation.html')
    
def index(request, *args, **kwargs):
    """Default index page"""
    return render(request, 'index.html')

def datasets(request, *args, **kwargs):
    """Datasets page"""
    return render(request, 'datasets.html', {
        'datasets': Dataset.objects.all()
        })

def dataset(request, pk, *args, **kwargs):
    """Datasets page"""
    dataset = Dataset.objects.get(pk=pk)
    return render(request, 'dataset.html', {
        'dataset': dataset,
        'data': plot_to_uri(dataset.process())
        })

def databases(request, *args, **kwargs):
    """Return list of databases"""
    return JsonResponse({'dbs': get_databases()})

def attributes(request, database):
    """Return attributes from model and strip _1 and _2"""
    return JsonResponse({'attrs': get_database_attributes(database)})

@login_required
def add_dataset(request):
    _, _, filenames = next(walk("datasets"))
    filenames.remove('.gitignore')
    filenames = map(lambda x: x.split('.')[0], filenames)
    context = {
        'filenames': filenames
    }
    return render(request, 'add_dataset.html', context)

class SetupDatasetView(LoginRequiredMixin, FormView):
    template_name = "setup_dataset.html"
    form_class = SetupDatasetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['filename'] = self.kwargs.get('filename') + '.csv'
        return kwargs

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
