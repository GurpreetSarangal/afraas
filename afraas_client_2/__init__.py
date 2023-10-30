from .Camera import *
from .Project import *
from .Recognizer import *
import requests

import json
import base64



import cv2 as cv





def startUp():
    cam = Camera(0)
    frame = cam.getFrame()
    
    rec = Recognizer()

    return cam, rec



def standBy(camera, recognizer):
    window = Project()

    while True:
        frame = camera.getFrame()
        if len(frame) == 0:
            continue
        faces, frame_roi = recognizer.cropToFace(frame)
       
        temp_urls = []

        if len(faces) >= 0:

            for face in frame_roi:
                camera.mark(frame, face[0] , face[1], face[2] ,face[3])
            
            for i, face in enumerate(faces):
                cv.imwrite(r"afraas_client_2\resources\database\temp\temp_"+str(i)+".png", face)

                
                with open(r"afraas_client_2\resources\database\temp\temp_"+str(i)+".png", "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read())
                    # print(b64_string)
                    data = {
                        "image": str( b64_string)
                    }
                    data = json.dumps(data)
                    url = "http://127.0.0.1:8000/api/mark/"

                    response = requests.post(url, data=data)
                    json_data = response.text
                    # print(json_data)
                    data = json.loads(json_data)

                    if not data["success"]:
                        print("ERROR: ",data["error"])
                    
                    else:
                        print("User [",data["name"],f"] is marked {data['status']}")
                        print("Faces were marked")

                    

           
            
        window.dashboard(frame)
        if cv.waitKey(20) == ord("e"):
            
            break
        

def boot():
    cam, rec = startUp()
    standBy(camera= cam, recognizer= rec)

    

def mark_attendance(faces):
    url = "http://127.0.0.1:8000/api/mark/"
    

    data = {
        "faces": faces
    }
    print(data)
    # data = json.dumps(data)
    response = requests.post(url, data=data)
    json_data = response.text
    data = json.loads(json_data)

    if data["error"] != "":
        print("ERROR: ",data["error"])
    
    else:
        # print("User [",data["name"],f"] is marked {data['status']}")
        print("Faces were marked")

    
