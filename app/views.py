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

from app.models import Dataset
from collections import Counter
from app.matplot import plot_to_uri


# Create your views here.
def guide(request):
    return render(request, 'user_documentation.html')
    
def index(request, *args, **kwargs):
    return render(request, 'index.html', {
        'datasets': Dataset.objects.all()
        })

def dataset(request, slug, *args, **kwargs):
    """Datasets page"""
    dataset = Dataset.objects.get(slug=slug)
    return render(request, 'process.html', {
        'dataset': dataset
        })

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

def process(request, slug):
    """Return the algorithm function"""
    dataset = Dataset.objects.get(slug=slug)
    params = request.GET
    # TODO: validate data
    data = dataset.process(
            int(params.get('time')),
            int(params.get('clusters')),
            proximity=params.get('proxAttrs'),
            diversity=params.get('divAttrs')
            )
    return JsonResponse({
        'chart': plot_to_uri(data),
        'data': {}
        })
