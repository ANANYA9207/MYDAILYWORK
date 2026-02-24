import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Load models
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("model.yml")

names = np.load("names.npy", allow_pickle=True).item()

st.title("Face Recognition App")

uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded is not None:

    # Convert uploaded file to OpenCV format
    image = Image.open(uploaded).convert("RGB")
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize for detection
    h, w = img.shape[:2]
    scale = 800 / max(h, w)
    if scale < 1:
        img = cv2.resize(img, (int(w*scale), int(h*scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80,80)
    )

    if len(faces) == 0:
        st.write("No face detected")

    for (x,y,w,h) in faces:

        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi,(200,200))

        label, conf = recognizer.predict(roi)

        if conf < 85:
            name = names[label]
        else:
            name = "Unknown"

        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img,f"{name} ({round(conf,1)})",
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    # Show result in frontend
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    st.image(img, caption="Prediction")