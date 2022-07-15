import django_tables2 as tables
from main.models import *



#OverTime Approval Buttons
overtime_approval = """
            <a href="{% url 'overtime' %}" class="btn btn-success" role="button">Approval</a>
            <a href="{% url 'overtime' %}" class="btn btn-danger" role="button">Refusal</a>
            """

class AttendanceTable(tables.Table):
    worker_id = tables.Column(verbose_name='Worker')
    attendanceDate = tables.Column(verbose_name='Date')
    status = tables.Column(verbose_name='Status')
    in_dateTime = tables.Column(verbose_name='In Time')
    out_dateTime = tables.Column(verbose_name='Out Time')
    work_hours = tables.Column(verbose_name='Work Hours')
    lateTime = tables.Column(verbose_name='Late Time')
    overTime = tables.Column(verbose_name='Overtime')
    in_location = tables.Column(verbose_name='In Location')
    out_location = tables.Column(verbose_name='Out Location')
    class Meta:
        model=Attendance
        fields = ['worker_id','attendanceDate','status','in_dateTime','out_dateTime','work_hours','lateTime','overTime','in_location','out_location']
        exclude = ['id']


class OverTimeApproval(tables.Table):
    actions = tables.TemplateColumn(overtime_approval,verbose_name='')
    worker_id = tables.Column(verbose_name='Worker')
    attendanceDate = tables.Column(verbose_name='Date')
    status = tables.Column(verbose_name='Status')
    in_dateTime = tables.Column(verbose_name='In Time')
    out_dateTime = tables.Column(verbose_name='Out Time')
    work_hours = tables.Column(verbose_name='Work Hours')
    lateTime = tables.Column(verbose_name='Late Time')
    overTime = tables.Column(verbose_name='Overtime')
    in_location = tables.Column(verbose_name='In Location')
    out_location = tables.Column(verbose_name='Out Location')
    class Meta:
        model=Attendance
        fields = ['worker_id','attendanceDate','status','in_dateTime','out_dateTime','work_hours','lateTime','overTime']
        exclude = ['id','in_location','out_location']

