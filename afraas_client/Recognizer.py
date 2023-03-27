import cv2 as cv
import numpy as np
import os



class Recognizer:
    def __init__(self, 
                cascade=r"AFRAAS\resources\models\haar_face.xml", 
                model=r"AFRAAS\resources\models\face_trained.yml"):
        self.pathToCascade = cascade
        self.pathToModel = model
        self.pathToLabels = r"AFRAAS\resources\models\labels.npy"
        self.pathToFeatures = r"AFRAAS\resources\models\features.npy"
        try:
            self.cascade = cv.CascadeClassifier(self.pathToCascade)
            self.model = cv.face.LBPHFaceRecognizer_create()
            self.model.read(model)

            l = np.load(self.pathToLabels)
            self.labels = l.tolist()

            f = np.load(self.pathToFeatures, allow_pickle=True)
            self.features = f.tolist()

        except:
            message = "haar cascade or model is not found on the path provided"
            raise Exception(message)
        
        self.DIR = r'AFRAAS\resources\database\persons'
        self.people = []

        for i in os.listdir(self.DIR):
            self.people.append(i)
        
    def whoIs(self, Face_roi):
        Face_roi = cv.cvtColor(Face_roi, cv.COLOR_BGR2GRAY)
        label, confidence = self.model.predict(Face_roi)
        if confidence >= 50:
            return self.people[label], confidence
        else:
            return "", False
        
    def cropToFace(self, Frame):
        gray = cv.cvtColor(Frame, cv.COLOR_RGB2GRAY)
        # cv.imshow("testing", gray)
        frame_roi = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

        try:
            first_face_indices = frame_roi[0]
            self.x, self.y, self.w, self.h = first_face_indices
        except:
            return []
        
        # cv.imshow("test", Frame[self.y:self.y+self.h, self.x:self.x+self.w])
        return Frame[self.y:self.y+self.h, self.x:self.x+self.w]
        
    def prepareDataSet(self, face_roi, name):
        face_roi = cv.cvtColor(face_roi, cv.COLOR_BGR2GRAY)
        if name not in self.people:
            self.people.append(name)
            self.people.sort()

        label = self.people.index(name)

        # self.labels = np.load(self.pathToLabels)
        # self.features = np.load(self.pathToFeatures)

        self.features.append(face_roi)
        self.labels.append(label)


    def resetDataSet(self):
        l = np.load(self.pathToLabels)
        self.labels = l.tolist()

        f = np.load(self.pathToFeatures, allow_pickle=True)
        self.features = f.tolist()

    
    def saveChangedDataset(self):
        features = np.array(self.features, dtype='object')
        labels = np.array(self.labels)

        # pathL = os.path.abspath(self.pathToLabels)
        # print(pathL)
        # pathB = os.path.abspath(self.pathToFeatures)
        # print(pathB)

        # print(features, labels)

        np.save(self.pathToFeatures, features)
        np.save(self.pathToLabels, labels)
        self.trainRecognizer(features, labels)


    def trainRecognizer(self, feat_array, label_array):
        new_trained_model = cv.face.LBPHFaceRecognizer_create()
        
        new_trained_model.train(feat_array, label_array)

        self.model = new_trained_model
        self.model.save(self.pathToModel)
        
    def recompileDataSet(self):
        try:
            people = []
            features = []
            labels = []
            for i in os.listdir(self.DIR):
                people.append(i)
                pathToUser = os.path.join(self.DIR, i)
                label = people.index(i)

                for img in os.listdir(pathToUser):
                    imgPath = os.path.join(pathToUser, img)
                    img_arr = cv.imread(imgPath)
                    img_arr = cv.cvtColor(img_arr, cv.COLOR_BGR2GRAY)
                    features.append(img_arr)
                    labels.append(label)
            
            self.people = people        
            self.features = features
            self.labels = labels
            self.saveChangedDataset()
        except:
            message = "recompilation was unsuccessful"
            raise Exception(message)




        

       