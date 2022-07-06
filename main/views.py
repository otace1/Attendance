from django.shortcuts import render
from django_tables2 import Table
from .tables import AttendanceTable
from .models import *

# Create your views here.

def main_home(request):
    template = 'index.html'
    context = {}
    return render(request,template,context)


def attendance(request):
    template = 'attendance.html'
    # query = Attendance.objects.raw('SELECT idcargaison_id, MONTH(datereceptionlabo) as mois, YEAR(datereceptionlabo) as annee \
    #                                                FROM hydro_occ.enreg_laboreception \
    #                                                WHERE idcargaison_id = %s')
    table = AttendanceTable(Attendance.objects.all().order_by('-id'))
    context = {'table':table}
    return render(request,template,context)


