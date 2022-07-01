import django_tables2 as tables
from main.models import *

class AttendanceTable(tables.Table):
    class Meta:
        model=Attendance
        