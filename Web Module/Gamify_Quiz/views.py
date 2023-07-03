from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question
import json
from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy as np
import dlib
import pickle as pkl
from sklearnex.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

x, y = pkl.load(open(r'D:\Project\Website-Phoenix13\LearnersEd\Gamify_Quiz\dataset\samples.pkl', 'rb'))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)

std = StandardScaler()
std.fit(x_train)
x_train = std.transform(x_train)
x_val = std.transform(x_val)
x_test = std.transform(x_test)

def detect_face_points(image):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r"D:\Project\Website-Phoenix13\LearnersEd\Gamify_Quiz\models\shape_predictor_68_face_landmarks.dat")
    face_rect = detector(image, 1)
    if len(face_rect) != 1:
        return []

    dlib_points = predictor(image, face_rect[0])
    face_points = []
    for i in range(68):
        x, y = dlib_points.part(i).x, dlib_points.part(i).y
        face_points.append(np.array([x, y]))
    return face_points

def compute_features(face_points):
    assert (len(face_points) == 68), "len(face_points) must be 68"

    face_points = np.array(face_points)
    features = []
    for i in range(68):
        for j in range(i + 1, 68):
            features.append(np.linalg.norm(face_points[i] - face_points[j]))

    return np.array(features).reshape(1, -1)

def Predict(image, model):
    im = np.array(image)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    face_points = detect_face_points(im)

    if len(face_points) != 68:
        print("68 face landmarks not detected.")
        return

    features = compute_features(face_points)
    features = std.transform(features)
    y_pred = model.predict(features)

    _, pitch_pred, yaw_pred = y_pred[0]

    if pitch_pred >= 5 and yaw_pred > 0:
        return 'top left'
    elif pitch_pred >= 8 and yaw_pred < 0:
        return 'top right'
    elif pitch_pred <= 8 and yaw_pred > 0:
        return 'bottom left'
    else:
        return 'bottom right'


model = load_model(r'D:\Project\Website-Phoenix13\LearnersEd\Gamify_Quiz\models\model.h5')

@csrf_exempt
def gamify_quiz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        image_data = json_data.get('image_data')
        marks = json_data.get('coins')

        if marks != -1:
            print(marks)  # Handle the quiz marks as required (e.g., store in database)
            response = {'message': 'Quiz data received'}
            return JsonResponse(response)
        elif image_data:
            # Convert the base64-encoded image data to PIL Image
            image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

            # Perform any processing or DL model prediction with the image
            prediction_result = Predict(image, model)

            # Replace this dummy response with the actual response you want to send back
            response = {'prediction': prediction_result}

            return JsonResponse(response)
        else:
            # No image data received
            response = {'error': 'No image data received'}
            return JsonResponse(response, status=400)

    else:
        # Fetch quiz questions from the database
        questions = Question.objects.all()

        # Convert questions to a list of dictionaries
        question_list = []
        for question in questions:
            question_dict = {
                'text': question.text,
                'options': [
                    question.option1,
                    question.option2,
                    question.option3,
                    question.option4
                ],
                'answer': question.correct_answer
            }
            question_list.append(question_dict)

        # Convert question_list to a JSON string
        questions_json = json.dumps(question_list)

        # Pass the questions to the template
        return render(request, 'gamify-quiz.html', {'questions_json': questions_json})
