from django.conf import settings

from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from app.forms import SetupDatasetForm

from app.models import Dataset, DataFile
from app.matplot import plot_to_uri
from django.http import HttpResponseRedirect

from django.views.decorators.cache import never_cache

from app.tasks import seed_dataset

decorators = [never_cache, ]


# Create your views here.
def guide(request):
    return render(request, 'guide.html')


@never_cache
def index(request, *args, **kwargs):
    return render(request, 'index.html', {
        'datasets': Dataset.objects.all()
    })


@never_cache
def dataset(request, slug, *args, **kwargs):
    """Datasets page"""
    dataset = Dataset.objects.get(slug=slug)
    return render(request, 'datasets.html', {
        'dataset': dataset,
        'algorithms': [
            {'name': 'K-Means', 'parameters': ['clusters']},
            {'name': 'DBSCAN', 'parameters': ['neighborhoodSize']},
            {'name': 'Birch', 'parameters': ['branchingFactor', 'threshold']}
        ]
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


@method_decorator(decorators, name='dispatch')
class UpdateDatasetView(LoginRequiredMixin, UpdateView):
    template_name = "edit_dataset.html"
    model = Dataset
    fields = ['name', 'description']


@method_decorator(decorators, name='dispatch')
class DeleteDatasetView(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Dataset
    success_url = reverse_lazy('datafiles')


@method_decorator(decorators, name='dispatch')
class DeleteDataFileView(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = DataFile
    success_url = reverse_lazy('datafiles')


@method_decorator(decorators, name='dispatch')
class DatasetFileView(LoginRequiredMixin, CreateView):
    template_name = "datafiles.html"
    model = DataFile
    fields = ['name', 'file']
    success_url = reverse_lazy('datafiles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset_files'] = DataFile.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        with open(self.object.file.path) as f:
            self.object.number_of_lines = sum(1 for line in f)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(decorators, name='dispatch')
class SetupDatasetView(LoginRequiredMixin, FormView):
    template_name = "setup_dataset.html"
    form_class = SetupDatasetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['file_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = DataFile.objects.get(slug=self.kwargs.get('slug'))
        return context

    def form_valid(self, form):
        dataset = form.save()
        if settings.CELERY:
            seed_dataset.delay(dataset.id)
        else:
            seed_dataset(dataset.id)
        return redirect('edit', dataset.slug)
