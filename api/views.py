import io
import os
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import *
from main.models import *
from deepface import DeepFace
from PIL import Image
from .face_verify import verifyFace
import datetime
import base64
import numpy

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
    date = datetime.datetime.today()

    #Face verification
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    img1 = data['img']
    decod = base64.b64decode(img1)
    decod = Image.open(io.BytesIO(decod))
    np1 = numpy.array(decod)

    a = User.objects.all()
    for user in a:
        img_link = user.facedata
        img2 = img_link
        print(img2)
        decod1 = Image.open(user.facedata)
        np2 = numpy.array(decod1)
        resp = DeepFace.verify(np1, np2, model_name=models[0], distance_metric=metrics[2])
        resp = resp['verified']
        if resp is True:
            shift = user.shift_id
            shift = Shift.objects.get(id=shift)
            shiftInTime = shift.in_shift
            lateTime = date - shiftInTime.replace(tzinfo=None)

            if lateTime.total_seconds() > 0:
                lateTime = lateTime
                Attendance.objects.create(
                    worker_id=user,
                    attendanceDate=date,
                    lateTime=lateTime,
                )
                context = {
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'timein': date
                }
                return Response(context, status=status.HTTP_200_OK)

            Attendance.objects.create(
                worker_id=user,
                attendanceDate=date,
            )
            context = {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'timein': date
            }
            return Response(context, status=status.HTTP_200_OK)
    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


#Attendance processing checkout
@api_view(['POST'])
def attendanceCheckout(request):
    data = request.data
    date = datetime.datetime.today()

    # Face verification
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    img1 = data['img']
    decod = base64.b64decode(img1)
    decod = Image.open(io.BytesIO(decod))
    np1 = numpy.array(decod)

    a = User.objects.all()
    for user in a:
        img_link = user.facedata
        img2 = img_link
        print(img2)
        decod1 = Image.open(user.facedata)
        np2 = numpy.array(decod1)
        resp = DeepFace.verify(np1, np2, model_name=models[0], distance_metric=metrics[2])
        resp = resp['verified']
        if resp is True:
            shift = user.shift_id
            shift = Shift.objects.get(id=shift)
            shiftOutTime = shift.out_shift

            inAttendance = Attendance.objects.filter(worker_id=user).order_by('-in_dateTime')[:1]
            inAttendance = inAttendance.values()
            inAttendance = inAttendance[0]
            inTime = inAttendance['in_dateTime']
            inAttendance = inAttendance['id']

            # Calcul Over Time & WorkHours
            overTime = date - shiftOutTime.replace(tzinfo=None)

            # print(overTime)
            workHours = date.replace(tzinfo=datetime.timezone.utc) - inTime
            if overTime.total_seconds() > 0:
                overTime = overTime
                checkout = Attendance.objects.get(id=inAttendance)
                print(checkout)
                checkout.out_dateTime = date
                checkout.overTime = overTime
                checkout.work_hours = workHours
                checkout.save(update_fields=['out_dateTime', 'work_hours', 'overTime'])
                context = {
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'outTime': date,
                }
            return Response(context, status=status.HTTP_200_OK)
    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


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

    dataset = "/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/"

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
                resp = resp['verified']
                if resp is True:
                    # path = print (os.path.join(dataset,image))
                    context = {
                        'ver':True,
                    }
                    return Response(context, status=status.HTTP_302_FOUND)
    context = {'ver':False}
    return Response(context, status=status.HTTP_404_NOT_FOUND)


