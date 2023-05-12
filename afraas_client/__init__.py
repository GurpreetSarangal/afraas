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
        cam = Camera(0)
        frame = cam.getFrame()
        if frame == []:
            raise Exception
    except:
        cam = Camera(1)
    rec = Recognizer()

    return cam, rec



def standBy(camera, recognizer, status):
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
                        mark_attendance(label, status=status)
                        count = 0
                else:
                    count = 0
                prev_label = label
        window.dashboard(frame)
        if cv.waitKey(20) == ord("e"):
            break
        

def boot():
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
    cam, rec = startUp()
    standBy(camera= cam, recognizer= rec, status=status)

    

def mark_attendance(label, status):
    print(label)
    
    # url = "http://localhost:8000/api/mark/"
    # now = datetime.datetime.now()

    # data = {
    #     "label": label, 
    #     "time-stamp": now,
    #     "status": status,
    # }
    # response = requests.post(url, data=data)
    # json_data = response.text
    # data = json.loads(json_data)
    # if data["error"] != "":
    #     print("ERROR: ",data["error"])
    
    # else:
    #     print("User [",label,f"] is marked {status}")

def addNewFace(id):
    url = "http://localhost:8000/api/check_registered/"
    data = {
        "id" : id,
    }
    # response = requests.post(url, data=data)
    # print(response.text)
    response = requests.post(url, data=data)
    json_data = response.text
    data = json.loads(json_data)
    if data["error"] != "":
        print(data["error"])
        return
        
    

    camera, rec = startUp()
    # db_conn = db()
    
    camera.addNewFace(str(id)+"_"+data["content"])

def removeFace(name):
    camera, rec = startUp()
    camera.removeFace(name)
