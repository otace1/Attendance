import pyqrcode
import requests
from django.shortcuts import render, HttpResponse, redirect
from django_tables2 import Table, RequestConfig, LazyPaginator
from django.core.exceptions import BadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .tables import *
from main.models import *
from .forms import *


# Create your views here.
@login_required(login_url='loginPage')
def usersList(request):
    template ='userslist.html'
    table = UsersTable(User.objects.all().order_by('id'))
    RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                     "per_page": 10}).configure(table)
    context = {'table': table}
    return render(request, template, context)

@login_required(login_url='loginPage')
#Add user from Web interface
def addUser(request):
    template = 'useradd.html'
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        user = User.objects.all().order_by('-id')[0]
        user_id = user.id
        filename = str(user.facedata)
        print(user_id)
        image = user.facedata.open(mode='rb')
        url = "https://search.facex.io:8443/images/singleImage/"

        payload = {'user_id': '62c81adb7312e67dcfb98d3f',
                   'name': user_id}
        files = [
            ('image', (filename, image, 'application/octet-stream'))
        ]
        headers = {}
        api_resp = requests.request("POST", url, headers=headers, data=payload, files=files)
        if api_resp:
            return redirect('usersList')
        else:
            raise BadRequest

    context = {
        'form':form
    }
    return render(request, template, context)


@login_required(login_url='loginPage')
# Genere Client QRCode
def qrCode(request,pk):
    code = User.objects.get(id=pk)
    code = str(code.id)
    # # Code pour generer le QRCode
    qrobj = pyqrcode.create(code, encoding='utf-8')
    with open('test.png', 'wb') as f:
        qrobj.png(f, scale=10)
    image_data = open('test.png', 'rb').read()
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename=%s.png'
    return response


@login_required(login_url='loginPage')
# Edit user
def userEdit(request,pk):
    template = 'useredit.html'
    user = User.objects.get(id=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('usersList')
    context = {'form':form}
    return render(request,template,context)


@login_required(login_url='loginPage')
def userDelete(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('usersList')


@login_required(login_url='loginPage')
def userDeactivate(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save(update_fields=['is_active'])
    return redirect('usersList')


@login_required(login_url='loginPage')
def userActivate(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save(update_fields=['is_active'])
    return redirect('usersList')


@login_required(login_url='loginPage')
def usersearch(request):
    template = 'userslist.html'
    if request.method == 'POST':
        search = request.POST['search']
        table = UsersTable(User.objects.filter(Q(firstname=search)|Q(lastname =search)|Q(matricule=search)))
        RequestConfig(request, paginate={"paginator_class": LazyPaginator,
                                         "per_page": 10}).configure(table)
        context = {'table': table}
        return render(request, template, context)
    return redirect('usersList')

