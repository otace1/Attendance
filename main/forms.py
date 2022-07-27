from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Row, Reset, Column, Fieldset
from crispy_forms.bootstrap import Field, InlineField, FormActions, StrictButton, Div
from django.views import generic
from django.contrib.gis import forms as gis_forms
from mapwidgets.widgets import GooglePointFieldWidget
from .models import *
from .widget import DatePickerInput
from django import forms

class SearchByDate(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True),required=False, label='Employee Name')
    branche = forms.ModelChoiceField(queryset=OfficeLocation.objects.all(),required=False, label='Office Branch')
    start_date = forms.DateField(widget=DatePickerInput, required=False)
    end_date = forms.DateField(widget=DatePickerInput, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchByDate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_errors = True
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Div(
                Field('', css_class='form-group col-sm-2'),
                Field('user', css_class='form-group col-sm-2'),
                Field('branche', css_class='form-group col-sm-2'),
                Field('start_date', css_class='form-group col-sm-2'),
                Field('end_date', css_class='form-group col-sm-2'),
            ),
            FormActions(
                Submit('Search', 'Search', css_class='btn-success'),
            )
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
        self.helper.form_class = 'form-vertical'
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
        self.helper.form_class = 'form-vertical'
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


class OfficeForm(forms.ModelForm):
    # gps_location = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={'map_width': 1450, 'map_height': 400}))
    gps_location = gis_forms.PointField(widget=GooglePointFieldWidget)
    # gps_geofence = gis_forms.PolygonField(widget=gis_forms.OSMWidget(attrs={'map_width': 300, 'map_height': 300}))

    class Meta:
        model = OfficeLocation
        fields = ['location','timezone','gps_location']

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('location', css_class='form-group col-md-12 mb-0'),
                Field('timezone', css_class='form-group col-md-12 mb-0'),
            ),
            Column(
                Field('gps_location', css_class='form-group col-md-12 mb-0'),
            ),
            Row(

                FormActions(
                    Submit('ADD', 'ADD', css_class='btn btn-success'),
                    Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
                ),
            ),
        )

class OfficeEditForm(forms.ModelForm):
    # gps_location = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={'map_width': 1450, 'map_height': 400}))
    gps_location = gis_forms.PointField(widget=GooglePointFieldWidget)
    # gps_geofence = gis_forms.PolygonField(widget=gis_forms.OSMWidget(attrs={'map_width': 300, 'map_height': 300}))

    class Meta:
        model = OfficeLocation
        fields = ['location','timezone','gps_location']

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('location', css_class='form-group col-md-12 mb-0'),
                Field('timezone', css_class='form-group col-md-12 mb-0'),
            ),
            Column(
                Field('gps_location', css_class='form-group col-md-12 mb-0'),
            ),
            Row(

                FormActions(
                    Submit('ADD', 'ADD', css_class='btn btn-success'),
                    Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
                ),
            ),
        )

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role']

    def __init__(self,*args,**kwargs):
        super(RoleForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_show_labels = True
        self.helper.form_class = 'form-vertical'
        self.helper.label_class = 'col-md-12'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Column(
                Field('role', css_class='form-group col-md-12 mb-0'),
            ),
            FormActions(
                Submit('ADD', 'ADD', css_class='btn btn-success'),
                Reset('CLEAR', 'CLEAR', css_class='btn btn-danger'),
            ),
        )