from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response


def reports(request):
    return render_to_response("reports.html")