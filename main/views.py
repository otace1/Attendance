from django.shortcuts import render, redirect
from django_tables2 import Table, RequestConfig, LazyPaginator
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from django.db.models import Count
import re
from .tables import *
from .models import *
from .forms import SearchByDate, ShiftForm, ShiftEditForm, OfficeForm, RoleForm
import datetime
import datefinder

# Create your views here.
def main_home(request):
    template = 'dashboard.html'
    today = datetime.date.today()
    today_attendance = Attendance.objects.filter(worker_id__onleave=False, worker_id__is_active=True, attendanceDate=today, status='P').count()
    today_absent = Attendance.objects.filter(attendanceDate=today, status='A').count()
    is_onLeave = User.objects.filter(is_onLeave=True).count()

    context = {
        'today_attendance':today_attendance,
        'today_absent':today_absent,
        'is_onLeave':is_onLeave
    }
    return render(request,template,context)

#Attendace show table
def attendance(request):
    template = 'attendance.html'
    form = SearchByDate()
    table = AttendanceTable(Attendance.objects.all().order_by('-id'),template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport("xlsx", table,dataset_kwargs={"title":"Attendance Report"})
        return exporter.response("table.{}".format(export_format))
    context = {
        'table':table,
        'form':form
        }
    return render(request,template,context)

def overtime(request):
    template = 'overtime.html'
    form = SearchByDate()
    table = OverTimeApproval(Attendance.objects.filter(status="P",overtime_status="", overTime = not None).order_by('-id'),template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))
    context = {
        'table': table,
        'form': form
    }
    return render(request, template, context)


def shift(request):
    template = 'shift.html'
    table = ShiftTable(Shift.objects.all(),template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))
    context = {
        'table': table,
    }
    return render(request, template, context)

def shiftAdd(request):
    template = 'shiftAdd.html'
    form = ShiftForm(request.POST or None)
    if form.is_valid():
        shift = request.POST['shift']
        intime = request.POST['inshift']
        outtime = request.POST['outshift']

        a = Shift(shift=shift,in_shift=intime,out_shift=outtime)
        a.save()
        return redirect('shift')
    else:
        context = {
            'form':form
        }
        return render(request,template,context)

def shiftDelete(request,pk):
    shift = Shift.objects.get(id=pk)
    shift.delete()
    return redirect('shift')

def shiftEdit(request,pk):
    template = 'shiftEdit.html'
    shift = Shift.objects.get(id=pk)
    form = ShiftEditForm(request.POST or None, instance=shift)
    if form.is_valid():
        form.save()
        return redirect('shift')
    context = {'form':form}
    return render(request,template,context)

def leave(request):
    template ='leave.html'
    table = LeaveTables(User.objects.all(),template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))
    context = {
        'table': table,
    }
    return render(request, template, context)

#Research
def research(request):
    template = 'overtime.html'
    form = SearchByDate()

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if start_date:
            if end_date:
                data_range = Attendance.objects.filter(attendanceDate__range=[start_date,end_date]).order_by('-id')
                table = AttendanceTable(data_range,template_name="django_tables2/bootstrap-responsive.html")
                RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                                 "per_page": 10}).configure(table)

                export_format = request.GET.get("_export", None)
                if TableExport.is_valid_format(export_format):
                    exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
                    return exporter.response("table.{}".format(export_format))
                context = {
                    'form':form,
                    'table':table
                }
                return render(request, template,context)
            else:
                data_range = Attendance.objects.filter(attendanceDate=start_date).order_by('-id')
                table = AttendanceTable(data_range,template_name="django_tables2/bootstrap-responsive.html")
                RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                                 "per_page": 10}).configure(table)

                export_format = request.GET.get("_export", None)
                if TableExport.is_valid_format(export_format):
                    exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
                    return exporter.response("table.{}".format(export_format))
                context = {
                    'form': form,
                    'table': table
                }
                return render(request, template, context)
        else:
            return redirect('attendance')
    else:
        return redirect('attendance')


#Office Settings
def office(request):
    template = 'office.html'
    form = OfficeForm()
    table = OfficeTable(OfficeLocation.objects.all(),template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))
    context = {
        'table': table,
        'form':form
    }
    return render(request, template, context)

#Add office branches
def officeBranchAdd(request):
    template = 'brancheAdd.html'
    form = OfficeForm()
    if request.method == 'POST':
        location = request.POST['location']
        timezone = request.POST['timezone']
        gps_location = request.POST['gps_location']

        a = OfficeLocation.objects.create(
            location=location,
            timezone=timezone,
            gps_location=gps_location,
        )
        return redirect('office')
    else:
        context = {
            'form':form
        }
        return render(request,template,context)

def branchdelete(request,pk):
    to_delete = OfficeLocation.objects.get(id=pk)
    to_delete.delete()
    return redirect('office')

def role(request):
    template = 'roles.html'
    table = RoleTable(Role.objects.all(), template_name="django_tables2/bootstrap-responsive.html")
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))
    context = {
        'table': table,
    }
    return render(request, template, context)


def roleadd(request):
    template = 'roleadd.html'
    form = RoleForm()
    if request.method == 'POST':
        role = request.POST['role']
        a = Role.objects.create(
            role=role
        )
        return redirect('role')
    else:
        context = {'form':form}
        return render(request,template,context)

def roledelete(request,pk):
    role = Role.objects.get(id=pk)
    role.delete()
    return redirect('role')
