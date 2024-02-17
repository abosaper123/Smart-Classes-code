import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# تحميل النموذج
model = load_model(r"C:\Users\TC\OneDrive\Desktop\data\ISEF\keras_model.h5")

# تصنيف الطلاب
def classify_student(frame):
    # تحجيم الإطار إلى حجم يتوقعه النموذج
    img = cv2.resize(frame, (224, 224))

    # تحويل الصورة إلى تنسيق يمكن استخدامه من قبل النموذج
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # التنبؤ باستخدام النموذج
    predictions = model.predict(img_array)

    # تحويل التنبؤ إلى نص
    if predictions[0][0] > 0.5:
        return "try to cheat"
    else:
        return "not try to cheat"

# فتح الكاميرا
cap = cv2.VideoCapture(0)

while True:
    # قراءة الإطار من الكاميرا
    ret, frame = cap.read()

    # تصنيف الطالب
    result = classify_student(frame)

    # عرض النتيجة على الإطار
    cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # عرض الإطار الناتج
    cv2.imshow('No more cheating result ', frame)

    # كسر الحلقة عند الضغط على 'q'
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

# إطفاء الكاميرا وإغلاق كل النوافذ
cap.release()
cv2.destroyAllWindows()