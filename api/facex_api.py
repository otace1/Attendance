import requests
import json


#Verification function
def faceX(IMAGE1_URL,IMAGE2_URL):
    # you can get the user_id in user dashboard
    USER_ID = "62c81adb7312e67dcfb98d3f"

    # add image url
    IMAGE1_URL = IMAGE1_URL
    IMAGE2_URL = IMAGE2_URL

    print(IMAGE1_URL)
    print(IMAGE2_URL)

    # face compare url
    API_URL = "http://facexapi.com/compare_faces"
    payload = {"img_1": IMAGE1_URL,"img_2": IMAGE2_URL}
    headers = {"user_id": USER_ID ,"Content-Type":"application/json"}

    response = requests.request("POST", url=API_URL, headers=headers, data=payload)
    print (response.text)
    r = response.text
    return r