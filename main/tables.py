import django_tables2 as tables
from main.models import *

class AttendanceTable(tables.Table):
    # worker = tables.Column(verbose_name='Worker')
    # dateIn = tables.Column(verbose_name='Date')
    # timeIn = tables.Column(verbose_name='CheckIn Time')
    # timeOut = tables.Column(verbose_name='CheckOut Time')
    # workHours = tables.Column(verbose_name='Work Hours')
    # shift = tables.Column(verbose_name='Shift')
    # in_location = tables.Column(verbose_name='Late Time')
    # out_location = tables.Column(verbose_name='Overtime')
    class Meta:
        model=Attendance
        fields = ['worker_id','attendanceDate','in_dateTime','out_dateTime','work_hours','lateTime','overTime','in_location','out_location']
        exclude = ['id']
        