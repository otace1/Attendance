from django.shortcuts import render
from django_tables2 import Table, RequestConfig, LazyPaginator
from .tables import *
from main.models import *


# Create your views here.
def usersList(request):
    template ='userslist.html'
    table = UsersTable(User.objects.all().order_by('id'))
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    context = {'table': table}
    return render(request, template, context)


