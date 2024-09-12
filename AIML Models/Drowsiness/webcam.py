import cv2
import numpy as np
from PIL import Image, ImageDraw
import face_recognition
from tensorflow import keras

eye_model = keras.models.load_model('./dataset/drowsiness_detection.h5')

def eye_cropper(frame):
    facial_features_list = face_recognition.face_landmarks(frame)
    try:
        eye = facial_features_list[0]['left_eye']
    except:
        try:
            eye = facial_features_list[0]['right_eye']
        except:
            return None
    
    x_max = max([coordinate[0] for coordinate in eye])
    x_min = min([coordinate[0] for coordinate in eye])
    y_max = max([coordinate[1] for coordinate in eye])
    y_min = min([coordinate[1] for coordinate in eye])

    x_range = x_max - x_min
    y_range = y_max - y_min

    if x_range > y_range:
        right = round(.5*x_range) + x_max
        left = x_min - round(.5*x_range)
        bottom = round((((right-left) - y_range))/2) + y_max
        top = y_min - round((((right-left) - y_range))/2)
    else:
        bottom = round(.5*y_range) + y_max
        top = y_min - round(.5*y_range)
        right = round((((bottom-top) - x_range))/2) + x_max
        left = x_min - round((((bottom-top) - x_range))/2)

    cropped = frame[top:(bottom + 1), left:(right + 1)]

    cropped = cv2.resize(cropped, (80,80))
    image_for_prediction = cropped.reshape(-1, 80, 80, 3)

    return image_for_prediction

    
def predict(frame):
    image_for_prediction = eye_cropper(image)
    if image_for_prediction is None:
        return 'Yes'
    try:
        image_for_prediction = image_for_prediction/255.0
    except:
        print("Error")
    
    prediction = eye_model.predict(image_for_prediction)
    print(prediction)
    # Based on prediction, display either "Open Eyes" or "Closed Eyes"
    if prediction < 0.7:
        status = 'No'
    else:
        status = 'Yes'
    return status