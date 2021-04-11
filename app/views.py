from os import walk

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.forms import SetupDatasetForm

from app.models import Dataset
from collections import Counter
from app.matplot import plot_to_uri


# Create your views here.
def guide(request):
    return render(request, 'guide.html')
    
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

@api_view(['GET'])
def process(request, slug):
    """Return the algorithm function"""
    dataset = Dataset.objects.get(slug=slug)
    params = request.query_params
    # TODO: validate data
    data = dataset.process(
            int(params.get('time')),
            int(params.get('clusters')),
            proximity={
                'attributes': params.getlist('proximity_attributes'),
                'weights': params.getlist('proximity_weights')
            },
            diversity={
                'attributes': params.getlist('diversity_attributes'),
                'weights': params.getlist('diversity_weights')
            },
            )
    return Response({
        'chart': plot_to_uri(data),
        'data': {}
        })
