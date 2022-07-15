from django.shortcuts import render
from django_tables2 import Table, RequestConfig, LazyPaginator
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from .tables import *
from .models import *
from .forms import SearchByDate

# Create your views here.
def main_home(request):
    template = 'index.html'
    context = {}
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
        exporter = TableExport(export_format, table)
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

