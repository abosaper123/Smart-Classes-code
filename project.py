import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = load_model(r"C:\Users\TC\OneDrive\Desktop\data\ISEF\keras_model.h5")

def classify_student(frame):
    img = cv2.resize(frame, (224, 224))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)

    if predictions[0][0] > 0.5:
        return "not try to cheat"
    else:
        return " try to cheat"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    result = classify_student(frame)

    cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow('No more cheating result ', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()