from django.shortcuts import render, redirect
from django_tables2 import Table, RequestConfig, LazyPaginator
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from django.db.models import Count, Q, Sum
from django.contrib.auth.decorators import login_required
import re
from .tables import *
from .models import *
from .forms import SearchByDate, ShiftForm, ShiftEditForm, OfficeForm, RoleForm, OfficeEditForm
import datetime
import datefinder

# Create your views here.
@login_required(login_url='loginPage')
def main_home(request):
    template = 'dashboard.html'
    today = datetime.date.today()
    at_work = Attendance.objects.filter(status='P', attendanceDate=today).count()
    late_in = Attendance.objects.filter(attendanceDate=today, lateTime__isnull=False).count()
    total_employee = User.objects.count()
    today_absent = Attendance.objects.filter(attendanceDate=today, status='A').count()
    is_onLeave = User.objects.filter(is_onLeave=True).count()
    early_out = Attendance.objects.filter(earlyOut__isnull=False).count()

    context = {
        'early_out':early_out,
        'late_in':late_in,
        'at_work':at_work,
        'total_employee':total_employee,
        'today_absent':today_absent,
        'is_onLeave':is_onLeave,
    }
    return render(request,template,context)


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
def shiftDelete(request,pk):
    shift = Shift.objects.get(id=pk)
    shift.delete()
    return redirect('shift')


@login_required(login_url='loginPage')
def shiftEdit(request,pk):
    template = 'shiftEdit.html'
    shift = Shift.objects.get(id=pk)
    form = ShiftEditForm(request.POST or None, instance=shift)
    if form.is_valid():
        form.save()
        return redirect('shift')
    context = {'form':form}
    return render(request,template,context)


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
#Research
def research(request):
    template = 'research.html'
    form = SearchByDate()

    if request.method == 'POST':
        user = request.POST['user']
        branche = request.POST['branche']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        if user:
            if branche:
                if start_date:
                    if end_date:
                        # data_range = Attendance.objects.filter(attendanceDate__range=[start_date,end_date]).values('worker_id').annotate(Sum('work_hours'), Sum('overTime'), Sum('lateTime'))
                        data_range = Attendance.objects.filter(worker_id=user, worker_id__office=branche,attendanceDate__range=[start_date,end_date]).order_by('-id')
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
                        data_range = Attendance.objects.filter(worker_id=user, worker_id__office=branche,
                                                               attendanceDate=start_date).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                    if end_date:
                        data_range = Attendance.objects.filter(worker_id=user, worker_id__office=branche, attendanceDate=end_date
                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(worker_id=user, worker_id__office=branche,

                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                if start_date:
                    if end_date:
                        data_range = Attendance.objects.filter(worker_id=user,attendanceDate__range=[start_date,end_date]).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(worker_id=user,
                                                               attendanceDate=start_date).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                    if end_date:
                        data_range = Attendance.objects.filter(worker_id=user,
                                                               attendanceDate=end_date
                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(worker_id=user
                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
            if branche:
                if start_date:
                    if end_date:
                        data_range = Attendance.objects.filter(worker_id__office=branche,
                                                               attendanceDate__range=[start_date,end_date]
                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(worker_id__office=branche,
                                                               attendanceDate__range=start_date
                                                               ).order_by(
                            '-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                    if end_date:
                        data_range = Attendance.objects.filter(worker_id__office=branche, attendanceDate=start_date).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(worker_id__office=branche).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                if start_date:
                    if end_date:
                        data_range = Attendance.objects.filter(attendanceDate__range=[start_date,end_date]).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                        data_range = Attendance.objects.filter(attendanceDate__range=start_date).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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
                    if end_date:
                        data_range = Attendance.objects.filter(attendanceDate=end_date).order_by('-id')
                        table = AttendanceTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
def branchdelete(request,pk):
    to_delete = OfficeLocation.objects.get(id=pk)
    to_delete.delete()
    return redirect('office')



@login_required(login_url='loginPage')
def branchedit(request,pk):
    template = 'brancheEdit.html'
    office = OfficeLocation.objects.get(id=pk)
    form = OfficeEditForm(request.POST or None, instance=office)
    if form.is_valid():
        form.save()
        return redirect('office')
    context = {'form': form}
    return render(request, template, context)



@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
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


@login_required(login_url='loginPage')
def roledelete(request,pk):
    role = Role.objects.get(id=pk)
    role.delete()
    return redirect('role')


@login_required(login_url='loginPage')
def leavesearch(request):
    template = 'leave.html'
    if request.method == 'POST':
        search = request.POST['search']
        table = LeaveTables(User.objects.filter(Q(firstname=search) | Q(lastname=search) | Q(matricule=search)))
        RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                         "per_page": 10}).configure(table)
        context = {'table': table}
        return render(request, template, context)
    return redirect('leave')


def leaveactivate(request,pk):
    leave_activate = User.objects.get(id=pk)
    leave_activate.is_onLeave = True
    leave_activate.save(update_fields=['is_onLeave'])
    return redirect('leave')

def leavedeactivate(request,pk):
    leave_activate = User.objects.get(id=pk)
    leave_activate.is_onLeave = False
    leave_activate.save(update_fields=['is_onLeave'])
    return redirect('leave')


@login_required(login_url='loginPage')
def aggregatedreport(request):
    template = 'aggregated.html'

    try:
        start_date = request.session['start_date']
        end_date = request.session['end_date']

        if request.session['start_date']:
            if start_date:
                if end_date:
                    data_range = Attendance.objects.filter(attendanceDate__range=[start_date, end_date]).values(
                        'worker_id').annotate(Sum('work_hours'), Sum('overTime'), Sum('lateTime'))
                    table = AggregatedTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
                    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                                     "per_page": 10}).configure(table)

                    export_format = request.GET.get("_export", None)
                    if TableExport.is_valid_format(export_format):
                        exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
                        return exporter.response("table.{}".format(export_format))
                    context = {
                        'table': table
                    }
                    return render(request, template, context)
                else:
                    data_range = Attendance.objects.filter(attendanceDate=start_date).values('worker_id').annotate(
                        Sum('work_hours'), Sum('overTime'), Sum('lateTime'))
                    table = AggregatedTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
                    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                                     "per_page": 10}).configure(table)

                    export_format = request.GET.get("_export", None)
                    if TableExport.is_valid_format(export_format):
                        exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
                        return exporter.response("table.{}".format(export_format))
                    context = {
                        'table': table
                    }
                    return render(request, template, context)

            data_range = Attendance.objects.all().values('worker_id').annotate(
                Sum('work_hours'), Sum('overTime'), Sum('lateTime'))
            table = AggregatedTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
            RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                             "per_page": 10}).configure(table)

            export_format = request.GET.get("_export", None)
            if TableExport.is_valid_format(export_format):
                exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
                return exporter.response("table.{}".format(export_format))
            context = {
                'table': table
            }
            return render(request, template, context)
        return redirect('attendance')

    except:
        data_range = Attendance.objects.all().values('worker_id').annotate(
            Sum('work_hours'), Sum('overTime'), Sum('lateTime'))
        table = AggregatedTable(data_range, template_name="django_tables2/bootstrap-responsive.html")
        RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                         "per_page": 10}).configure(table)

        export_format = request.GET.get("_export", None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport("xlsx", table, dataset_kwargs={"title": "Attendance Report"})
            return exporter.response("table.{}".format(export_format))
        context = {
            'table': table
        }
        return render(request, template, context)


