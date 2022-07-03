from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from main.models import *
from datetime import date, datetime

# Create your views here.
@api_view(['GET'])
def getUser(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserDetails(request,pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    data = request.data
    role = data['role']
    office = data['office']
    role = Role.objects.get(id=role)
    office = OfficeLocation.objects.get(id=office)
    user = User.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        surname=data['surname'],
        role=role,
        office=office,
        facedata=data['facedata']
    )
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request,pk):
    data = request.data
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('User deleted!')

@api_view(['POST'])
def attendanceCheckin(request):
    today = date.today()
    data = request.data
    inTime = data['in_time']
    outTime = data['out_time']
    FMT = '%H:%M:%S'
    work_hours = datetime.strptime(outTime,FMT) - datetime.strptime(inTime,FMT)

    user = User.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        surname=data['surname'],
        # role=role,
        # office=office,
        facedata=data['facedata']
    )
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getRole(request):
    role = Role.objects.all()
    serializer = UserSerializer(role, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOffice(request):
    office = OfficeLocation.objects.all()
    serializer = UserSerializer(office, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRole(request):
    role = Role.objects.all()
    serializer = UserSerializer(role, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getShift(request):
    shift = Shift.objects.all()
    serializer = UserSerializer(shift, many=True)
    return Response(serializer.data)