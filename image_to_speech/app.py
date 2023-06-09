from flask import Flask, render_template, request, Response, jsonify
from PIL import Image
import pytesseract
import cv2
import pyttsx3
import base64
import os


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def capture_frames():
    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

def recognize_text(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

def convert_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'static/output.mp3')
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image_data = request.form['image']
    image_data = image_data.replace('data:image/png;base64,', '')
    image_data = base64.b64decode(image_data)

    # Save the image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image.png')
    with open(image_path, 'wb') as f:
        f.write(image_data)

    text = recognize_text(image_path)
    convert_to_speech(text)
    return jsonify({'text': text})

@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
