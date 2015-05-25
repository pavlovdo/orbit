__author__ = 'pavlov'

from django.forms import ModelForm
from models import Network


class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = ['ip', 'netmask']
