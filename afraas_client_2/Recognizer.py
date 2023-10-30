import cv2 as cv
import numpy as np
import os



class Recognizer:
    def __init__(self, 
                cascade=r"afraas_client\resources\models\haar_face.xml", ):
        self.pathToCascade = cascade
        
        try:
            self.cascade = cv.CascadeClassifier(self.pathToCascade)
        except:
            message = "haar cascade is not found on the path provided"
            raise Exception(message)
        self.DIR = r'afraas_client\resources\database\persons'
        
        
        
    def cropToFace(self, Frame):
        gray = cv.cvtColor(Frame, cv.COLOR_RGB2GRAY)
        
        frame_roi = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)
        faces = []
        

        try:
            for face_indices in frame_roi:
                self.x, self.y, self.w, self.h = face_indices
                faces.append(Frame[self.y:self.y+self.h, self.x:self.x+self.w])
        except:
            return []
        
        
        return faces, frame_roi
        
    