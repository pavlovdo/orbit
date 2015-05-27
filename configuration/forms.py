__author__ = 'pavlov'

from django.forms import ModelForm
from django import forms
from models import Network


#class NetworkForm(forms.Form):
#    your_name = forms.CharField(label='Your name', max_length=100)

class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = ['name','ip', 'netmask',]
