import io
import os
import json
import requests
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from main.models import *
from deepface import DeepFace
from PIL import Image, ImageDraw, ImageFont
import datetime
import base64
import numpy

# #Win Azure FaceId
# from azure.cognitiveservices.vision.face import FaceClient
# from msrest.authentication import CognitiveServicesCredentials

#Open key Files for Azure
credential = json.load(open('AzureKey.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']
ENDPOINT_VERIFY = ENDPOINT+'face/v1.0/verify'


class UserCreate(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = list()
            context.append({
                'status': 200,
                'message':'user created successfuly'
            })
            user = User.objects.all().order_by('-id')[0]
            user_id = user.id
            filename = str(user.facedata)
            print(user_id)
            image = user.facedata.open(mode='rb')
            url = "https://search.facex.io:8443/images/singleImage/"

            payload = {'user_id': '62c81adb7312e67dcfb98d3f',
                       'name': user_id}
            files = [
                ('image', (filename, image, 'application/octet-stream'))
            ]
            headers = {}
            api_resp = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(api_resp)
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getUserDetails(request,pk):
    user = User.objects.get(id=pk)
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
    in_time = datetime.datetime.today()
    date = in_time.date()
    in_time = in_time.time()
    date_temp = datetime.date(1, 1, 1)
    url = "https://search.facex.io:8443/auth/searchWithEncodedImage"
    img1 = data['img']
    payload = {
        "image_encoded": img1,
        "user_id": "62c81adb7312e67dcfb98d3f"
    }
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    stat = data['status']
    # Face verification
    # models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    # metrics = ["cosine", "euclidean", "euclidean_l2"]
    # backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    # img1 = data['img']
    # decod = base64.b64decode(img1)
    # decod = Image.open(io.BytesIO(decod))
    # np1 = numpy.array(decod)
    #
    # a = User.objects.all()
    # for user in a:
    #     img_link = user.facedata
    #     img2 = img_link
    #     print(img2)
    #     decod1 = Image.open(user.facedata)
    #     np2 = numpy.array(decod1)
    #     resp = DeepFace.verify(np1, np2, model_name=models[0], distance_metric=metrics[2])
    #     resp = resp['verified']
    #     if resp is True:
    if stat == 'ok':
        data = data['data']
        u = data['user']
        r = u[0]
        matricule = r['person_name']
        print(matricule)
        user = User.objects.get(id=matricule)

        shift = user.shift_id
        shift = Shift.objects.get(id=shift)
        shiftInTime = shift.in_shift
        shiftOutTime = shift.out_shift

        datetime1 = datetime.datetime.combine(date_temp,in_time)
        datetime2 = datetime.datetime.combine(date_temp,shiftInTime)
        lateTime = datetime1 - datetime2

            #Identification de presence
        d1 = datetime.datetime.combine(date_temp,shiftInTime)
        d2 = datetime.datetime.combine(date_temp,shiftOutTime)
        d3 = d2-d1

        if lateTime.total_seconds() > d3.total_seconds():
            status_presence = 'A'
        else:
            status_presence = 'P'

        if lateTime.total_seconds() > 0:
            lateTime = lateTime
            Attendance.objects.create(
                            worker_id=user,
                            attendanceDate=date,
                            in_dateTime= in_time,
                            lateTime=lateTime,
                            status=status_presence,
                    )
            context = {
                            'id': user.id,
                            'firstname': user.firstname,
                            'lastname': user.lastname,
                            'timein': in_time
                        }
            return Response(context, status=status.HTTP_200_OK)
        else:
            Attendance.objects.create(
                            worker_id=user,
                            attendanceDate=date,
                            in_dateTime=in_time,
                            status=status_presence,
                        )
            context = {
                            'id': user.id,
                            'firstname': user.firstname,
                            'lastname': user.lastname,
                            'timein': in_time
                        }
            return Response(context, status=status.HTTP_200_OK)
    context = {
                'message':'User not found'
            }
    return Response(context, status=status.HTTP_404_NOT_FOUND)


# #Attendance processing checkout
@api_view(['POST'])
def attendanceCheckout(request):
    data = request.data
    out_time = datetime.datetime.today()
    out_time = out_time.time()
    date_temp = datetime.date(1, 1, 1)
    url = "https://search.facex.io:8443/auth/searchWithEncodedImage"
    img1 = data['img']
    payload = {
        "image_encoded": img1,
        "user_id": "62c81adb7312e67dcfb98d3f"
    }
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    stat = data['status']
    # models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    # metrics = ["cosine", "euclidean", "euclidean_l2"]
    # backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    # img1 = data['img']
    # decod = base64.b64decode(img1)
    # decod = Image.open(io.BytesIO(decod))
    # np1 = numpy.array(decod)
    #
    # a = User.objects.all()
    # for user in a:
    #     img_link = user.facedata
    #     img2 = img_link
    #     print(img2)
    #     decod1 = Image.open(user.facedata)
    #     np2 = numpy.array(decod1)
    #     resp = DeepFace.verify(np1, np2, model_name=models[0], distance_metric=metrics[2])
    #     resp = resp['verified']
    #     if resp is True:
    if stat == 'ok':
        data = data['data']
        u = data['user']
        r = u[0]
        matricule = r['person_name']
        user = User.objects.get(id=matricule)

        shift = user.shift_id
        shift = Shift.objects.get(id=shift)
        shiftOutTime = shift.out_shift

        a = Attendance.objects.filter(worker_id=user).order_by('-id')[0]
        b = a.id
        in_time = a.in_dateTime
        in_time = datetime.datetime.combine(date_temp, in_time)

            #Overtime calculation
        datetime1 = datetime.datetime.combine(date_temp, out_time)
        datetime2 = datetime.datetime.combine(date_temp, shiftOutTime)
        overTime = datetime1 - datetime2
        print(overTime)

            #Worktime calculation
        workhours = datetime1 - in_time

        if overTime.total_seconds() > 0:
            checkout = Attendance.objects.get(id=b)
            checkout.out_dateTime = out_time
            checkout.overTime = overTime
            checkout.work_hours = workhours
            checkout.save(update_fields=['out_dateTime', 'work_hours', 'overTime'])
            context = {
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'out_time': out_time,
                }
            return Response(context, status=status.HTTP_200_OK)
        else:
            checkout = Attendance.objects.get(id=b)
            checkout.out_dateTime = out_time
            checkout.work_hours = workhours
            checkout.save(update_fields=['out_dateTime', 'work_hours'])
            context = {
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'out_time': out_time,
                }
            return Response(context, status=status.HTTP_200_OK)
    context={
                'message':'User not found'
                }
    return Response(context, status=status.HTTP_404_NOT_FOUND)



# @api_view(['POST'])
# def verifyFace(request):
#     models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
#     metrics = ["cosine", "euclidean", "euclidean_l2"]
#     backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
#
#     data = request.data
#     img1 = data['img']
#     decod = base64.b64decode(img1)
#     decod = Image.open(io.BytesIO(decod))
#     np1 = numpy.array(decod)
#
#     dataset = "/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/"
#
#     # with open(img1, "rb") as img1_file:
#     #     binary = img1_file.read()
#     #     img1_b64 = base64.b64encode(binary)
#     #     img1_b64 = img1_b64.decode('utf-8')
#     #     decod = base64.b64decode(img1_b64)
#     #     decod = Image.open(io.BytesIO(decod))
#     #     np1 = numpy.array(decod)
#     #
#     # with open(img2, "rb") as img2_file:
#     #     binary = img2_file.read()
#     #     img2_b64 = base64.b64encode(binary)
#     #     img2_b64 = img2_b64.decode('utf-8')
#     #     decod = base64.b64decode(img2_b64)
#     #     decod = Image.open(io.BytesIO(decod))
#     #     np2 = numpy.array(decod)
#
#     for image in os.listdir(dataset):
#         # if (image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
#         if (image.endswith(".jpg") or image.endswith(".jpeg")):
#             img2 = os.path.join(dataset,image)
#             with open(img2, "rb") as img2_file:
#                 binary = img2_file.read()
#                 img2_b64 = base64.b64encode(binary)
#                 img2_b64 = img2_b64.decode('utf-8')
#                 decod1 = base64.b64decode(img2_b64)
#                 decod1 = Image.open(io.BytesIO(decod1))
#                 np2 = numpy.array(decod1)
#                 resp = DeepFace.verify(np1,np2,model_name=models[0], distance_metric=metrics[2])
#                 resp = resp['verified']
#                 if resp is True:
#                     # path = print (os.path.join(dataset,image))
#                     context = {
#                         'ver':True,
#                     }
#                     return Response(context, status=status.HTTP_302_FOUND)
#     context = {'ver':False}
#     return Response(context, status=status.HTTP_404_NOT_FOUND)


