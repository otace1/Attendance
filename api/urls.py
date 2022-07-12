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
    #User mgmt and creation
    # path('users/list/', getUser, name='getUser'),
    path('users/', UserCreate.as_view(), name='createUserandGet'),
    path('users/<int:pk>/details/', getUserDetails, name='getUserDetails'),
    path('users/<int:pk>/update/', updateUser, name='updateUser'),
    path('users/<int:pk>/delete/', deleteUser, name='deleteUser'),

    # Shift setup
    path('users/shift/', getShift, name='getShift'),

    #Office Setup
    path('users/office/', getOffice, name='getOffice'),
    path('users/office/create/', createOffice, name='createOffice'),

    #Users Roles
    path('users/role/', getRole, name='getRole'),

    #Attendance processingß
    path('attendance/checkin/', attendanceCheckin, name='attendanceCheckin'),
    path('attendance/checkout/', attendanceCheckout, name='attendanceCheckout'),

    #VerifyFaces
    path('faceverification/verify/', verifyFace, name='verifyFace'),

]
