from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Row, Reset, Column, Fieldset
from crispy_forms.bootstrap import Field, InlineField, FormActions, StrictButton
from django.views import generic
from main.models import *
from django import forms
from django.forms import ModelForm

#Edit User
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('firstname','lastname','surname','job','matricule','shift','office','role','facedata','is_active')
        labels = {
            'Firstname':'',
            'Lastname':'',
            'Surname':'',
            'Job':'',
            'Matricule':'',
            'Shift':'',
            'Office':'',
            'Role':'',
            'facedata':''
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-verical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('firstname', css_class='form-group col-md-12 mb-0'),
                Field('lastname', css_class='form-group col-md-12 mb-0'),
                Field('surname', css_class='form-group col-md-12 mb-0'),
            ),
            Column(
                Field('job', css_class='form-group col-md-6 mb-0'),
                Field('matricule', css_class='form-group col-md-6 mb-0'),
            ),
            Column(
                Field('shift', css_class='form-group col-md-6 mb-0'),
                Field('office', css_class='form-group col-md-6 mb-0'),
                Field('role', css_class='form-group col-md-6 mb-0'),
            ),
            Column(
                Field('facedata', css_class='form-group col-md-12 mb-0'),
                Field('is_active', css_class='form-group col-md-12 mb-0'),
            ),

            FormActions(
                Submit('ADD', 'ADD', css_class='btn btn-success'),
                Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
            ),
        )


# class EditUserForm(forms.Form):
#     firstname = forms.CharField()
#     lastname = forms.CharField()
#     surname = forms.CharField()
#     job = forms.CharField()
#     matricule = forms.CharField()
#     shift = forms.ModelChoiceField(queryset=Shift.objects.all())
#     office = forms.ModelChoiceField(queryset=OfficeLocation.objects.all())
#     role = forms.ModelChoiceField(queryset=Role.objects.all())
