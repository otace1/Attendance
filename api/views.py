import io
import os
import glob
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from main.models import *
from deepface import DeepFace
from PIL import Image
import datetime
import base64
import numpy
import pandas as pd


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
    json_data = list()
    json_data.append({
        'status':200,
        'data':
            {
                'firstname': data['firstname'],
                'lastname': data['lastname'],
                'surname': data['surname'],
                'role': data['role'],
                'office': data['office'],
                'facedata': data['facedata']
            } })
    serializer = UserSerializer(user, many=False)
    return Response(json_data,status=status.HTTP_200_OK)

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
    serializer = RoleSerializer(role, many=True)
    return Response(serializer.data)

#Office processing
@api_view(['GET'])
def getOffice(request):
    office = OfficeLocation.objects.all()
    serializer = OfficeSerializer(office, many=True)
    return Response(serializer.data)

#Shift
@api_view(['GET'])
def getShift(request):
    shift = Shift.objects.all()
    serializer = ShiftSerializer(shift, many=True)
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

@api_view(['POST'])
def verifyFace(request):
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

    data = request.data
    img1 = data['img']
    decod = base64.b64decode(img1)
    decod = Image.open(io.BytesIO(decod))
    np1 = numpy.array(decod)

    # img1 = "/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/bill-gates-jpg.jpeg"
    # img2 = "/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/Elon2.jpg"
    dataset = "/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/"

    # img2 = User.objects.get(id=1)
    # img2 = img2.facedata
    # decod = base64.b64decode(img2)
    # decod =Image.open(io.BytesIO(decod))
    # np2 = numpy.array(decod)

    # with open(img1, "rb") as img1_file:
    #     binary = img1_file.read()
    #     img1_b64 = base64.b64encode(binary)
    #     img1_b64 = img1_b64.decode('utf-8')
    #     decod = base64.b64decode(img1_b64)
    #     decod = Image.open(io.BytesIO(decod))
    #     np1 = numpy.array(decod)
    #
    # with open(img2, "rb") as img2_file:
    #     binary = img2_file.read()
    #     img2_b64 = base64.b64encode(binary)
    #     img2_b64 = img2_b64.decode('utf-8')
    #     decod = base64.b64decode(img2_b64)
    #     decod = Image.open(io.BytesIO(decod))
    #     np2 = numpy.array(decod)

    for image in os.listdir(dataset):
        # if (image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
        if (image.endswith(".jpg") or image.endswith(".jpeg")):
            img2 = os.path.join(dataset,image)
            with open(img2, "rb") as img2_file:
                binary = img2_file.read()
                img2_b64 = base64.b64encode(binary)
                img2_b64 = img2_b64.decode('utf-8')
                decod1 = base64.b64decode(img2_b64)
                decod1 = Image.open(io.BytesIO(decod1))
                np2 = numpy.array(decod1)
                resp = DeepFace.verify(np1,np2,model_name=models[0], distance_metric=metrics[2])
                print (resp['verified'])
                # if resp == "True":
                #     context = {'ver':True,}
                #     return Response(context, status=status.HTTP_302_FOUND)

    # df = DeepFace.find(np1,db_path=db, model_name=models[1],distance_metric=metrics[2])
    # df = df.head()
    # resp = DeepFace.verify(np1,np2,model_name=models[0], distance_metric=metrics[2])
    # ver = resp['verified']
    # print(ver)
    context = {'ver':False,}
    return Response(status=status.HTTP_404_NOT_FOUND)


