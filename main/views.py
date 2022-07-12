from django.shortcuts import render
from django_tables2 import Table, RequestConfig, LazyPaginator
from .tables import AttendanceTable
from .models import *

# Create your views here.

def main_home(request):
    template = 'index.html'
    context = {}
    return render(request,template,context)


def attendance(request):
    template = 'attendance.html'
    table = AttendanceTable(Attendance.objects.all().order_by('-id'))
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    context = {'table':table}
    return render(request,template,context)


