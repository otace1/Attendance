"""AttendanceFP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('home/', main_home, name='main_home'),
    path('attendance/', attendance, name='attendance'),
    path('attendance/overtime/', overtime, name='overtime'),
    path('shift/', shift, name='shift'),
    path('shift/add/', shiftAdd, name='shiftAdd'),
    path('shift/<int:pk>/delete/', shiftDelete, name='shiftDelete'),
    path('shift/<int:pk>/edit/', shiftEdit, name='shiftEdit'),
    path('leave/', leave, name='leave'),

    path('office/', office, name='office'),
    path('office/new/branch/', officeBranchAdd, name='officeBranchAdd'),
    path('office/branch/<int:pk>/delete/', branchdelete, name='branchdelete'),

    path('role/', role, name='role'),
    path('role/add/', roleadd, name='roleadd'),
    path('role/<int:pk>/delete/', roledelete, name='roledelete'),

    #Reseach
    path('research/', research, name='research'),

]
