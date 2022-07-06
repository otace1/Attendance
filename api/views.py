from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from main.models import *
import datetime

# User processing
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
    try:
        user = User.objects.create(
            firstname=data['firstname'],
            lastname=data['lastname'],
            surname=data['surname'],
            role=role,
            office=office,
            facedata=data['facedata']
        )
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)

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


#Role processing
@api_view(['GET'])
def getRole(request):
    role = Role.objects.all()
    serializer = UserSerializer(role, many=True)
    return Response(serializer.data)

#Office processing
@api_view(['GET'])
def getOffice(request):
    office = OfficeLocation.objects.all()
    serializer = UserSerializer(office, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def createOffice(request):
    office = OfficeLocation.objects.all()
    serializer = UserSerializer(office, many=True)
    return Response(serializer.data)

#Attendance processing checkin
@api_view(['POST'])
def attendanceCheckin(request):
    data = request.data
    try:
        user=User.objects.get(id=data['worker_id'])
    except:
        return Response({'detail':'User not found'},status=status.HTTP_404_NOT_FOUND)

    checkin = Attendance.objects.create(
        worker_id=user
    )
    serializer = AttendanceSerializer(checkin, many=False)
    return Response(serializer.data)

#Attendance processing checkout
@api_view(['POST'])
def attendanceCheckout(request):
    out_time = datetime.datetime.now()
    data = request.data
    try:
        user = User.objects.get(id=data['worker_id'])
        print(user)
        inattendance = Attendance.objects.filter(worker_id=user).order_by('-in_dateTime')[:1]
        inattendance = inattendance.values()
        inattendance = inattendance[0]
        inattendance = inattendance['id']
    except:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    checkout = Attendance.objects.get(id=inattendance)
    checkout.out_dateTime = out_time
    checkout.save(update_fields=['out_dateTime'])
    serializer = AttendanceSerializer(checkout, many=False)
    return Response(serializer.data)





