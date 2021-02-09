from django.shortcuts import render
from app.algos import example_algo, gabe

# Create your views here.
def index(request, *args, **kwargs):
    context = {
        'example_data': example_algo()[:10]
    }
    context['data'] = gabe.run(['mass0_1', 'lumin_1'])
    return render(request, 'index.html', context)
