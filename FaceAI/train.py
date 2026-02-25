import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces=[]
labels=[]
names={}
label_id=0

dataset="dataset"

for person in os.listdir(dataset):

    person_path=os.path.join(dataset,person)

    if not os.path.isdir(person_path):
        continue

    print("Reading:",person)

    names[label_id]=person

    for file in os.listdir(person_path):

        path=os.path.join(person_path,file)
        img=cv2.imread(path)

        if img is None:
            print("Skipping unreadable:",file)
            continue

        # ---- RESIZE LARGE IMAGES FIRST (IMPORTANT) ----
        h,w=img.shape[:2]
        scale=800/max(h,w)
        if scale<1:
            img=cv2.resize(img,(int(w*scale),int(h*scale)))

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        detected=face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(40,40)
        )

        if len(detected)==0:
            print("No face found:",file)
            continue

        for (x,y,w,h) in detected:

            face=gray[y:y+h,x:x+w]
            face=cv2.resize(face,(200,200))

            faces.append(face)
            labels.append(label_id)

    label_id+=1

print("Total faces collected:",len(faces))

if len(faces)==0:
    print("ERROR: No training data found")
    exit()

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces,np.array(labels))
recognizer.save("model.yml")

np.save("names.npy",names)

print("Training complete")