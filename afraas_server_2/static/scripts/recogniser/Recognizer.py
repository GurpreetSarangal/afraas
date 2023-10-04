import cv2 as cv
import numpy as np
import os



class Recognizer:
    def __init__(self, 
                cascade=r"afraas_client\resources\models\haar_face.xml", 
                model=r"afraas_client\resources\models\face_trained.yml"):
        self.pathToCascade = cascade
        self.pathToModel = model
        self.pathToLabels = r"afraas_client\resources\models\labels.npy"
        self.pathToFeatures = r"afraas_client\resources\models\features.npy"
        try:
            self.cascade = cv.CascadeClassifier(self.pathToCascade)
            
            
            

        except:
            message = "haar cascade is not found on the path provided"
            raise Exception(message)
        
        try:
            self.model = cv.face.LBPHFaceRecognizer_create()
            self.model.read(model)
            l = np.load(self.pathToLabels)
            self.labels = l.tolist()
            # print(self.labels)

            f = np.load(self.pathToFeatures, allow_pickle=True)
            self.features = f.tolist()
            # print(self.features)
        except:
            rec = Recognizer()
            rec.recompileDataSet()
            self.model = cv.face.LBPHFaceRecognizer_create()
            self.model.read(model)
            l = np.load(self.pathToLabels)
            self.labels = l.tolist()
            # print(self.labels)

            f = np.load(self.pathToFeatures, allow_pickle=True)
            self.features = f.tolist()
            # print(self.features)

        self.DIR = r'afraas_client\resources\database\persons'
        self.people = []

        for i in os.listdir(self.DIR):
            # print(i)
            self.people.append(i)
        
    def whoIs(self, Face_roi):
        Face_roi = cv.cvtColor(Face_roi, cv.COLOR_BGR2GRAY)
        # cv.imshow("test", Face_roi)
        label, confidence = self.model.predict(Face_roi)
        # print(label, confidence)
        if confidence >= 55 and confidence <= 95:
            # print(self.people[label], confidence)
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
            print(self.people)

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
        # print(self.pathToModel)
        self.model.save(self.pathToModel)
        
    def recompileDataSet(self):
        try:
            people = []
            features = []
            labels = []
            for i in os.listdir(self.DIR):
                people.append(i)
                people.sort()
                pathToUser = os.path.join(self.DIR, i)
                label = people.index(i)
                # print(self.DIR, i , label)
                for img in os.listdir(pathToUser):
                    # print(" - - -  ", img)
                    imgPath = os.path.join(pathToUser, img)
                    
                    img_arr = cv.imread(imgPath)
                    img_arr = cv.cvtColor(img_arr, cv.COLOR_BGR2GRAY)
                    img_arr = np.array(img_arr,'uint8')
                    features.append(img_arr)
                    labels.append(label)
            
            # print(people, labels)
            self.people = people        
            self.features = features
            self.labels = labels
            self.saveChangedDataset()
        except:
            message = "recompilation was unsuccessful"
            raise Exception(message)




        

       