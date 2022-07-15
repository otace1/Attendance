from django.shortcuts import render, redirect
from django_tables2 import Table, RequestConfig, LazyPaginator
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from django.db.models import Count
from .tables import *
from .models import *
from .forms import SearchByDate, ShiftForm, ShiftEditForm
import datetime

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
    table = AttendanceTable(Attendance.objects.all().order_by('-id'))
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)

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
    table = OverTimeApproval(Attendance.objects.filter(status="P",overtime_status="", overTime = not None).order_by('-id'))
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)

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
    table = ShiftTable(Shift.objects.all())
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
    table = LeaveTables(User.objects.all())
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

