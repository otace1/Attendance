from django.shortcuts import render

# Create your views here.

def main_home(request):
    template = 'index.html'
    context = {}
    return render(request,template,context)


def attendance(request):
    template = 'attendance.html'

