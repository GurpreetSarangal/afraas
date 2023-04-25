import cv2 as cv
import shutil
import numpy as np
import os
from .Recognizer import Recognizer
from .Project import Project


class Camera:
    def __init__(self, cam):
        self.AllModes = [(0, cv.CAP_DSHOW), (1, None)]
        self.SelectedMode = self.AllModes[cam]
        self.pathToCascade = r"afraas_client\resources\models\haar_face.xml"
        self.pathToRecognizer = r"afraas_client\resources\models\face_trained.yml"
        self.pathToDatabase = r"afraas_client\resources\database\persons"
        if cam==1:
            self.capture = cv.VideoCapture(self.SelectedMode[0])
        else:
            self.capture = cv.VideoCapture(self.SelectedMode[0], self.SelectedMode[1])
        
        self.absPath = os.path.abspath('')
        
        
        
        
        

    def connect(self):
        if self.SelectedMode[1] == None:
            capture = cv.VideoCapture(self.SelectedMode[0])
        else:
            capture = cv.VideoCapture(self.SelectedMode[0], self.SelectedMode[1])
        
        return capture

    def getFrame(self):
        isRead, Frame = self.capture.read()
        if isRead:
            return Frame
        else:
            return []
        
        
    
        

    def toGrayScale(self, Frame):
        return cv.cvtColor(Frame, cv.COLOR_BGR2GRAY)
    
    def saveImg(self, Frame, name):

        cv.imwrite(f"{name}.jpg", Frame)

    def addNewFace(self, name):
        try:
            id = len(os.listdir(self.pathToDatabase)) + 1
        except:
            message = "given path is not found"
            raise Exception(message)

        name_with_id = str(id) + "_" + name
        # print(name_with_id)
        pathForNewFace = os.path.join(self.pathToDatabase, name_with_id)

        # print(pathForNewFace)
        
        # ! check if user is already registered or not
        
        recognizer = Recognizer()
        window = Project()

        os.mkdir(pathForNewFace)
        os.chdir(pathForNewFace)
        # self.connect()
        tempId = 1
        threshold = -1
        try:
            while True:
                # print(threshold)
                if threshold >= 100:
                    message = "Person is not in frame"
                    raise Exception(message)
                    # print("not in frame")
                
                frame = self.getFrame()
                if frame == []:
                    message = "Maybe camera was disconnected"
                    raise Exception(message)

                     
                   
                face = recognizer.cropToFace(frame)
                

                if(face == [] ):
                    # print("not in frame")
                    if threshold >= 0:
                        threshold += 1
                    
                else:             
                    self.saveImg(face, name_with_id+"_"+str(tempId))
                    tempId += 1
                    self.mark(frame, 
                            "saving as "+name_with_id+"_"+str(tempId), 
                            recognizer.x, 
                            recognizer.y, 
                            recognizer.w, 
                            recognizer.h)
                    threshold = 0
                    recognizer.prepareDataSet(face, name_with_id)

                window.registerNewFace(frame)
                if tempId >= 100 or cv.waitKey(20) == ord('e') :
                    break
            os.chdir(self.absPath)
            recognizer.saveChangedDataset()
        except Exception as e:  
            os.chdir(self.absPath)
            shutil.rmtree(pathForNewFace)
            recognizer.resetDataSet()
            print(e)
        finally:

            cv.destroyAllWindows()
        
    def test_Cam(self):
        # self.connect()
        while(True):
            frame = self.getFrame()
            cv.imshow("test", frame)
            rec = Recognizer()
            # rec.cropToFace(frame)
            cropped = rec.cropToFace(frame)
            if cropped != []:
                cv.imshow("face", cropped)
            if cv.waitKey(20) == ord('e'):
                break

    def updateFace(self, name):

        pass

    def removeFace(self, name):
        pathForNewFace = os.path.join(self.pathToDatabase, name)
        shutil.rmtree(pathForNewFace)
        rec = Recognizer()
        rec.recompileDataSet()

        
    
    def mark(self, Frame, label, x, y, w, h):
        cv.putText(Frame, str(label), (x, y+h+30), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), thickness=2)
        cv.rectangle(Frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)
    
    def __del__(self):      
        self.capture.release()
        cv.destroyAllWindows()
