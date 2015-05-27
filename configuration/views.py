# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf

from .forms import NetworkForm
from .models import Network

def configuration(request):
    args = {}
    args.update(csrf(request))
    args['networks'] = Network.objects.all()
    args['network_form'] = NetworkForm
    return render_to_response("configuration.html", args)


def addnetwork(request):
    if request.POST and ("pause" not in request.session):
        form = NetworkForm(request.POST)
        if form.is_valid():
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/configuration')