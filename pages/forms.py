# pages/forms.py

from django import forms
from .models import Ticker


class TickerForm(forms.ModelForm):
    class Meta:
        model = Ticker
        fields = ['text']
