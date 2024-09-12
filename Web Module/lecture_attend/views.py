from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
import base64
import json
import face_recognition
from tensorflow import keras
import cv2
import numpy as np

eye_model = keras.models.load_model(r'D:\Project\Website-Phoenix13\LearnersEd\lecture_attend\model\drowsiness_detection.h5')


def eye_cropper(frame):
    frame_np = np.array(frame)  # Convert PIL image to NumPy array
    frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR (if necessary)

    gray = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
    facial_features_list = face_recognition.face_landmarks(gray)

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
        right = round(.5 * x_range) + x_max
        left = x_min - round(.5 * x_range)
        bottom = round((((right - left) - y_range)) / 2) + y_max
        top = y_min - round((((right - left) - y_range)) / 2)
    else:
        bottom = round(.5 * y_range) + y_max
        top = y_min - round(.5 * y_range)
        right = round((((bottom - top) - x_range)) / 2) + x_max
        left = x_min - round((((bottom - top) - x_range)) / 2)

    cropped = frame_np[top:(bottom + 1), left:(right + 1)]

    cropped = cv2.resize(cropped, (80, 80))
    image_for_prediction = cropped.reshape(-1, 80, 80, 3)

    return image_for_prediction


def predict(frame):
    image_for_prediction = eye_cropper(frame)
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

@csrf_exempt
def lecture_attend(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        image_data = json_data.get('image_data')
        if image_data:
            # Convert the base64-encoded image data to PIL Image
            image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

            # Perform any processing or DL model prediction with the image
            prediction_result = predict(image)

            # Replace this dummy response with the actual response you want to send back
            response = {'prediction': prediction_result}

            return JsonResponse(response)
        else:
            # No image data received
            response = {'error': 'No image data received'}
            return JsonResponse(response, status=400)
    return render(request, 'lectures-attend.html', {})
