import django_tables2 as tables
from main.models import *



#OverTime Approval Buttons
overtime_approval = """
            <a href="{% url 'overtime' %}" class="btn btn-success" role="button">Approval</a>
            <a href="{% url 'overtime' %}" class="btn btn-danger" role="button">Refusal</a>
            """

#OverTime Approval Buttons
shift_button = """
            <a href="{% url 'shiftEdit' record.pk %}" class="btn btn-success" role="button">Edit</a>
            <a href="{% url 'shiftDelete' record.pk %}" class="btn btn-danger" role="button">Delete</a>
            """

#Leave buttons
leave_button = """
            <a href="{% url 'shiftEdit' record.pk %}" class="btn btn-success" role="button">Activate</a>
            <a href="{% url 'shiftEdit' record.pk %}" class="btn btn-danger" role="button">Deactivate</a>
            """

#Office buttons
office_button = """
            <a href="{% url 'shiftEdit' record.pk %}" class="btn btn-success" role="button">Edit</a>
            <a href="{% url 'branchdelete' record.pk %}" class="btn btn-danger" role="button">Delete</a>
            """

#Role buttons
role_button = """
            <a href="" class="btn btn-success" role="button">Edit</a>
            <a href="{% url 'roledelete' record.pk %}" class="btn btn-danger" role="button">Delete</a>
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


class ShiftTable(tables.Table):
    actions = tables.TemplateColumn(shift_button,verbose_name='')
    shift = tables.Column(verbose_name='Shift Name')
    in_shift = tables.Column(verbose_name='In Time')
    out_shift = tables.Column(verbose_name='Out Time')
    class Meta:
        model=Shift
        fields = ['shift','in_shift','out_shift','actions']


class LeaveTables (tables.Table):
    actions = tables.TemplateColumn(leave_button, verbose_name='')
    office = tables.Column(verbose_name='Affectation')
    job = tables.Column(verbose_name='Job Title')

    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'job', 'office', 'shift', 'is_onLeave', 'actions']
        exclude = ['facedata', 'role','is_active']

class OfficeTable (tables.Table):
    actions = tables.TemplateColumn(office_button, verbose_name='')
    class Meta:
        model = OfficeLocation
        fields = ['id','location','timezone','gps_location']

class RoleTable (tables.Table):
    actions = tables.TemplateColumn(role_button, verbose_name='')
    class Meta:
        model = Role
        fields = ['id','role']


class AggregatedTable (tables.Table):
    class Meta:
        model = Attendance
        fields = ['worker_id','attendanceDate','status','in_dateTime','out_dateTime','work_hours','lateTime','overTime','in_location','out_location']
        exclude = ['id']
