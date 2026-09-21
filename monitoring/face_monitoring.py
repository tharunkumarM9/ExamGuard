#for monitoring the face presence here we use a machine learning method called haar cascade 
# this method id useful for detecting the object in the vedio or image
# haar cascades detector is a simple rectangular patterns called haarer features
#  image > simple check > more detailed check > classifier > object detected
# haar cascade looks for the patterns of light and the dark regions that resemble the object it trained to reconize. # it is fast and easy to reconize
# import cv2
# def start_face_monitoring():
#     #load face detector 
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


#     #open camera
#     camera = cv2.videocapture(0)

#     while True

#for monitoring the face presence here we use a machine learning method called haar cascades
#this method id useful for detecting the object in the vedio or image
#haar cascades detector is a simple reactangular patterns called harrer features 
#image > simple check >more detailed checks > classifer >objected detected
#haar cascade looks for the patterns of light and the dark regions that resemble the object it trained to reconize.It is fast and easy to use .

import cv2
import numpy as np


# ----------------------------------------
# LOAD FACE DETECTOR
# ----------------------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ----------------------------------------
# DETECT FACE
# ----------------------------------------
def detect_face(image_data):

    # Convert image bytes into NumPy array
    image_array = np.frombuffer(
        image_data,
        dtype=np.uint8
    )


    # Convert image array into OpenCV image
    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )


    # Check whether image was decoded
    if image is None:
        return False, None


    # ----------------------------------------
    # CONVERT TO GRAYSCALE
    # ----------------------------------------
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ----------------------------------------
    # DETECT FACES
    # ----------------------------------------
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )


    # ----------------------------------------
    # DRAW FACE RECTANGLE
    # ----------------------------------------
    for (x, y, w, h) in faces:

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        return True, image


    # No face detected
    return False, image