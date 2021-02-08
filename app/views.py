from django.shortcuts import render
from django.views import FormView
from app.algos import example_algo
from app.forms import AlgoRequestForm

# Create your views here.
def index(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    return render(request, 'index.html', context)

def AlgoRequestView(FormView):
    form_class = AlgoRequestForm

    