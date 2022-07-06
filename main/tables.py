import django_tables2 as tables
from main.models import *

class AttendanceTable(tables.Table):
    class Meta:
        model=Attendance
        fields = ['worker_id','in_dateTime','out_dateTime','in_location','out_location']
        exclude = ['id']
        