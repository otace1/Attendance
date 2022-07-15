from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.views import generic
from .models import *
from django import forms

class SearchByDate(forms.Form):
    date_start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
