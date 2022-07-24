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
    path('users/web/', usersList, name='usersList'),
    path('users/web/user/add/', addUser, name='addUser'),
    path('users/web/user/<int:pk>/qrcode/', qrCode, name='qrCode'),
    path('users/web/user/<int:pk>/edit/', userEdit, name='userEdit'),
    # path('users/web/user/<int:pk>/delete/', userDelete, name='userDelete'),
    path('users/web/user/<int:pk>/deactivated/', userDeactivate, name='userDeactivate'),
    path('users/web/user/<int:pk>/activate/', userActivate, name='userActivate'),

    path('users/web/user/search/', usersearch, name='usersearch'),


]
