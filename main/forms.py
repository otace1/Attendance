from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Row, Reset, Column, Fieldset
from crispy_forms.bootstrap import Field, InlineField, FormActions, StrictButton
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


class ShiftEditForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift','in_shift','out_shift']

    def __init__(self, *args, **kwargs):
        super(ShiftEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-verical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('shift', css_class='form-group col-md-12 mb-0'),
            ),
            Column(
                Field('in_shift', css_class='form-group col-md-6 mb-0'),
                Field('out_shift', css_class='form-group col-md-6 mb-0'),
            ),

            FormActions(
                Submit('ADD', 'ADD', css_class='btn btn-success'),
                # Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
            ),
        )


class ShiftForm(forms.Form):
    shift = forms.CharField(label="Shift Name")
    inshift = forms.TimeField(label="Shift InTime")
    outshift = forms.TimeField(label="Shift OutTime")

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-verical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('shift', css_class='form-group col-md-12 mb-0'),
            ),
            Column(
                Field('inshift', css_class='form-group col-md-6 mb-0'),
                Field('outshift', css_class='form-group col-md-6 mb-0'),
            ),

            FormActions(
                Submit('ADD', 'ADD', css_class='btn btn-success'),
                Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
            ),
        )