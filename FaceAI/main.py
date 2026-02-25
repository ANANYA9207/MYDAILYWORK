import cv2
import numpy as np

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

)
print("loaded successfully")
# Load trained recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("model.yml")

# Load names dictionary
names = np.load("names.npy", allow_pickle=True).item()

# -------- GET IMAGE PATH --------
path = input("Enter image path: ")
img = cv2.imread(path)

if img is None:
    print("Image not found or unsupported format")
    exit()

# -------- RESIZE LARGE IMAGE FOR BETTER DETECTION --------
h, w = img.shape[:2]
scale = 800 / max(h, w)
if scale < 1:
    img = cv2.resize(img, (int(w*scale), int(h*scale)))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -------- FACE DETECTION (TUNED) --------
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(80,80)   # prevents eye/ear detection
)

if len(faces) == 0:
    print("No face detected")
else:
    print("Faces detected:", len(faces))

# -------- RECOGNITION --------
for (x, y, w, h) in faces:

    # extra safety to skip tiny detections
    if w < 80 or h < 80:
        continue

    roi = gray[y:y+h, x:x+w]

    # resize exactly like training
    roi = cv2.resize(roi, (200, 200))

    label, conf = recognizer.predict(roi)

    # lower conf = better match
    if conf < 85:
        name = names[label]
    else:
        name = "Unknown"

    # draw box + name
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.putText(img, f"{name} ({round(conf,1)})",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0,255,0), 2)

cv2.imshow("Face Recognition", img)
cv2.waitKey(0)
cv2.destroyAllWindows()