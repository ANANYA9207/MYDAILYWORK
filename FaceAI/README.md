# Face Recognition Application using OpenCV

## 📌 Project Overview
This project is an AI-based Face Recognition system that detects and recognizes human faces from images.  
It uses OpenCV’s Haar Cascade classifier for face detection and the LBPH (Local Binary Pattern Histogram) algorithm for face recognition.

The system allows users to:
- Train a model using a dataset of labeled face images
- Upload an image and identify the person in the image
- View detected faces with predicted names and confidence scores

---

## Technologies Used
- Python  
- OpenCV  
- NumPy  
- Streamlit (for frontend UI)

---
## 📊 Dataset
The dataset contains folders for each person.  
Each folder includes multiple images of that person.

Example:dataset/
musk/
1.jpg
2.jpg
modi/
1.jpg
2.jpg

## How to Run the Project?

1. Open Terminal or Anaconda Prompt and go to the project folder:

   cd C:\Users\Ananya\FaceAI

2. Install the required libraries (run once):

   pip install opencv-contrib-python numpy streamlit pillow

3. Train the face recognition model:

   python train.py

   This will generate:
   - model.yml
   - names.npy

4. Run face recognition using Python:

   python main.py

   Enter the image path when prompted, for example:
   dataset/musk/1.jpg

   The program will detect the face and display the predicted name.

5. (Optional) Run the frontend interface:

   streamlit run app.py

   Open the browser link shown (usually http://localhost:8501)  
   Upload an image to see the prediction.

**Notes**
- Keep all training images inside the `dataset/` folder.
- Each person must have a separate subfolder.
- Use JPG or PNG images only.
- Run `train.py` again if new images are added.

## How It Works?
1. Images from the dataset are loaded and converted to grayscale.
2. Haar Cascade detects faces in each image.
3. Faces are resized and used to train the LBPH recognizer.
4. During prediction:
   - Faces are detected in the input image
   - Each face is compared with trained data
   - The predicted name is displayed with confidence value.

---

## ✅ Features
- Face detection using Haar Cascade
- Face recognition using LBPH algorithm
- Works on uploaded images
- Simple browser-based UI using Streamlit
- Easy dataset expansion

---

## 📌 Future Improvements
- Real-time webcam recognition
- Deep learning-based face detection
- Better UI design
- Model accuracy improvements

  ## License
This project is for educational and internship demonstration purposes.


