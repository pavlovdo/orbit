__author__ = 'pavlov'

from django.shortcuts import render
# Create your views here.
from django.shortcuts import render_to_response


def home(request):
    name = 'Orbit'
    return render_to_response('main.html', {'name': name})
