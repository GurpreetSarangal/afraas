import cv2 as cv

import os



class Camera:
    def __init__(self, cam):
        self.AllModes = [(0, cv.CAP_DSHOW), (1, None)]
        self.SelectedMode = self.AllModes[cam]
        self.pathToCascade = r"afraas_client\resources\models\haar_face.xml"
        self.pathToRecognizer = r"afraas_client\resources\models\face_trained.yml"
        self.pathToDatabase = r"afraas_client\resources\database\persons"
        if cam==1:
            self.capture = cv.VideoCapture(self.SelectedMode[1])
        else:
            self.capture = cv.VideoCapture(self.SelectedMode[0])
           
        
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
    
   
    
    def mark(self, Frame, x, y, w, h):
        cv.putText(Frame, "Detected", (x, y+h+30), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), thickness=2)
        cv.rectangle(Frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)
    
    def __del__(self):      
        self.capture.release()
        cv.destroyAllWindows()
