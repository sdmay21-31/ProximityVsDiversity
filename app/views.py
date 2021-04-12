from os import walk
import os

from django.conf import settings

from django.apps import apps
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.forms import SetupDatasetForm, UploadFileForm

from app.models import Dataset, DatasetFile
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

class DatasetFileView(LoginRequiredMixin, CreateView):
    template_name = "add_dataset.html"
    model = DatasetFile
    fields = ['name', 'file']
    success_url = '/add'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset_files'] = DatasetFile.objects.all()
        return context

class UpdateDatasetView(LoginRequiredMixin, UpdateView):
    template_name = "edit_dataset.html"
    model = Dataset
    fields = ['name', 'description']

class SetupDatasetView(LoginRequiredMixin, FormView):
    template_name = "setup_dataset.html"
    form_class = SetupDatasetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['file_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = DatasetFile.objects.get(slug=self.kwargs.get('slug'))
        return context

    def form_valid(self, form):
        dataset = form.save()
        seed_dataset.delay(dataset.id)
        return redirect('dataset_status', dataset.slug)
