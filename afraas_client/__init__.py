from .Camera import *
from .Project import *
from .Recognizer import *
from db import db

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
            label, confidence = recognizer.whoIs(face)
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
        window.dashboard(frame)
        if cv.waitKey(20) == ord("e"):
            break
        

def boot():
    
    cam, rec = startUp()
    standBy(camera= cam, recognizer= rec)


def mark_attendance(label):
    print(label)

def addNewFace(name):
    camera, rec = startUp()
    db_conn = db()
    
    camera.addNewFace(name.lower())

def removeFace(name):
    camera, rec = startUp()
    camera.removeFace(name)
