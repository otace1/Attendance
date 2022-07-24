from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginPage(request):
    template = 'login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('main_home')
        else:
            return redirect('loginPage')
    return render(request, template)

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
def userRegistration(request):
    template ='register.html'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('usersList')
    else:
        context = {'form':form}
        return render(request,template,context)







