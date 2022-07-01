from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from main.models import *

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': 'main/registration/',
            'method': 'POST',
            'body': None,
            'description': 'User Registration'
        },
        {
            'Endpoint':'main/attendance/checkin',
            'method': 'POST',
            'body': None,
            'description': 'Save Checkin'
        },
        {
            'Endpoint': 'main/attendance/checkout',
            'method': 'POST',
            'body': None,
            'description': 'Save Checkout'
        }
    ]
    return Response(routes)

@api_view(['GET'])
def getLeavetypes(request):
    leaveTypes = LeaveTypes.objects.all()
    serializer = LeaveTypesSerializer(leaveTypes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getLeavetype(request,pk):
    leaveType = LeaveTypes.objects.get(id=pk)
    serializer = LeaveTypesSerializer(leaveType, many=False)
    return Response(serializer.data)


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
