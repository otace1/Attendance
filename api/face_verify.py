from deepface import DeepFace
from PIL import Image
from main.models import User
from rest_framework.decorators import api_view
import base64
import numpy
import io
import os

@api_view()
def verifyFace(img):
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
    img1 = img
    decod = base64.b64decode(img1)
    decod = Image.open(io.BytesIO(decod))
    np1 = numpy.array(decod)

    #Get users to iterate with
    a = User.objects.all()
    for user in a:
        img_link = user.facedata
        print(img_link)
        img2 = img_link
        with open(img2,"rb") as img2_file:
            binary = img2_file.read()
            img2_b64 = base64.b64encode(binary)
            img2_b64 = img2_b64.decode('utf-8')
            decod1 = base64.b64decode(img2_b64)
            decod1 = Image.open(io.BytesIO(decod1))
            np2 = numpy.array(decod1)
            resp = DeepFace.verify(np1, np2, model_name=models[0], distance_metric=metrics[2])
            resp = resp['verified']
            if resp is True:
                return a
    return False


    # for image in os.listdir(dataset):
    #     # if (image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
    #     if (image.endswith(".jpg") or image.endswith(".jpeg")):
    #         img2 = os.path.join(dataset,image)
    #         with open(img2, "rb") as img2_file:
    #             binary = img2_file.read()
    #             img2_b64 = base64.b64encode(binary)
    #             img2_b64 = img2_b64.decode('utf-8')
    #             decod1 = base64.b64decode(img2_b64)
    #             decod1 = Image.open(io.BytesIO(decod1))
    #             np2 = numpy.array(decod1)
    #             resp = DeepFace.verify(np1,np2,model_name=models[0], distance_metric=metrics[2])
    #             resp = resp['verified']
    #             if resp is True:
    #                 # path = print (os.path.join(dataset,image))
    #                 context = {
    #                     'ver':True,
    #                 }
    #                 return Response(context, status=status.HTTP_302_FOUND)
    # context = {'ver':False}
    # return Response(context, status=status.HTTP_404_NOT_FOUND)