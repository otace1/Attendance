from django.shortcuts import render, redirect

# Create your views here.

def login(request):
    template = 'login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        return redirect('main_home')
    return render(request, template)



def logout(request):
    pass