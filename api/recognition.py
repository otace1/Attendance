import base64
import io
import numpy
from PIL import Image

img = '/Users/cedric/PycharmProjects/AttendanceFP/api/dataset/Cedric Taty.png'

with open(img, "rb") as img2_file:
    binary = img2_file.read()
    img2_b64 = base64.b64encode(binary)
    img2_b64 = img2_b64.decode('utf-8')
    decod = base64.b64decode(img2_b64)
    decod = Image.open(io.BytesIO(decod))
    np2 = numpy.array(decod)

print(img2_b64)





