from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response, redirect

def index(request):
    args = {}
    return render_to_response('management.html', args)
