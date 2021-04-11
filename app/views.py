from os import walk
import os

from django.conf import settings

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.forms import SetupDatasetForm, UploadFileForm

from app.models import Dataset
from collections import Counter
from app.matplot import plot_to_uri

from app.tasks import seed_dataset


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

@login_required
def add_dataset(request):
    _, _, filenames = next(walk("datasets"))
    filenames.remove('.gitignore')
    context = {
        'filenames': filenames,
        'form': UploadFileForm
    }
    return render(request, 'add_dataset.html', context)

def handle_uploaded_file(f):
    splt = f.name.split('.')
    extension = splt[-1]
    name = '_'.join(splt[:-1])
    filename = '.'.join([slugify(name), extension])
    with open(os.path.join(settings.BASE_DIR, 'datasets', filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
    return redirect('/add')

class SetupDatasetView(LoginRequiredMixin, FormView):
    template_name = "setup_dataset.html"
    form_class = SetupDatasetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['filename'] = self.kwargs.get('filename')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filename'] = self.kwargs.get('filename')
        return context

    def form_valid(self, form):
        dataset = form.save()
        seed_dataset(dataset, self.kwargs.get('filename'))
        return redirect('dataset-processing', dataset)
