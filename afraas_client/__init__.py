from .Camera import *
from .Project import *
from .Recognizer import *
import requests
import datetime
import json

# from db import db

import mysql.connector
import cv2 as cv



# def initiate():
#     project = Project()
#     project.

# def test(c=1):
#     cam = Camera(c)
#     cam.test_Cam()

def startUp():
    try:
        cam = Camera(1)
        frame = cam.getFrame()
        if frame == []:
            raise Exception
    except:
        cam = Camera(0)
    rec = Recognizer()

    return cam, rec



def standBy(camera, recognizer):
    window = Project()
    prev_label = ''
    count = 0
    while True:
        frame = camera.getFrame()
        # print(frame)
        # cv.imshow("frame", frame)
        face = recognizer.cropToFace(frame)
        if len(face) > 0:
            # cv.imshow("face", face)
            # print("face dected")
            label, confidence = recognizer.whoIs(face)
            # print(label, confidence)
            if confidence:
                camera.mark(frame, label, recognizer.x,recognizer.y,recognizer.w,recognizer.h)
                if label == prev_label:
                    count += 1
                    if count >= 3:
                        mark_attendance(label)
                        count = 0
                else:
                    count = 0
                prev_label = label
            else:
                camera.mark(frame, prev_label, recognizer.x,recognizer.y,recognizer.w,recognizer.h)

        window.dashboard(frame)
        if cv.waitKey(20) == ord("e"):
            break
        

def boot():
    
    cam, rec = startUp()
    standBy(camera= cam, recognizer= rec)

    

def mark_attendance(label):
    cv.destroyAllWindows()
    print("please specify the status to be marked: ")
    print("1: enter")
    print("2: exit")
    ch = int(input())
    if ch==1:
        status = "enter"
    elif ch==2:
        status = "exit"
    else:
        print("wrong selection")
        return
    

    url = "http://localhost:8000/api/mark/"
    now = datetime.datetime.now()

    data = {
        "label": label, 
        "time-stamp": now,
        "status": status,
    }
    response = requests.post(url, data=data)
    json_data = response.text
    data = json.loads(json_data)
    if data["error"] != "":
        print("ERROR: ",data["error"])
    
    else:
        print("User [",label,f"] is marked {status}")

def addNewFace(id):

    url = "http://localhost:8000/api/check_registered/"
    data = {
        "id" : id,
    }
    response = requests.post(url, data=data)
    json_data = response.text
    data = json.loads(json_data)
    if not data["success"]:
        print(data["error"])
        return
        
    camera, rec = startUp()
    name = data["content"]
    camera.addNewFace(str(id)+"_"+data["content"])

    url = "http://localhost:8000/api/mark_face_registered/"
    data = {
        "id" : id,
    }
    response = requests.post(url, data=data)
    json_data = response.text
    res = json.loads(json_data)

    if not res["success"]:
        print(res["error"])
    else:
        print(f"#{id} {name} is successfully registred")
        

def removeFace(id):
    camera, rec = startUp()
    camera.removeFace(id)

    url = "http://localhost:8000/api/mark_face_unregistered/"
    data = {
        "id" : id,
    }
  
    response = requests.post(url, data=data)
    json_data = response.text
    data = json.loads(json_data)
    if not data["success"]:
        print(data["error"])
        return
