from flask import Flask, render_template, request, Response, jsonify
from PIL import Image
import pytesseract
import cv2
import pyttsx3
import base64
import os
import numpy as np
import pyopencl as cl
from numba import njit, cuda
import pyopencl.tools as cl_tools
import sycl

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def capture_frames():
    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@sycl.kernel
def recognize_text(image, output):
    idx = sycl.get_global_id(0)
    output[idx] = pytesseract.image_to_string(image[idx])

@sycl.kernel
def convert_to_speech(text, output):
    idx = sycl.get_global_id(0)
    engine = pyttsx3.init()
    engine.save_to_file(text[idx], 'static/output_{}.mp3'.format(idx))
    engine.runAndWait()
    output[idx] = 1

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

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    platforms = cl.get_platforms()
    devices = platforms[0].get_devices()
    ctx = cl.Context(devices)
    queue = cl.CommandQueue(ctx)

    # Create SYCL buffers
    image_buffer = sycl.buffer(img)
    text_buffer = sycl.buffer(np.zeros(1, dtype=np.int32))
    speech_buffer = sycl.buffer(np.zeros(1, dtype=np.int32))

    # Enqueue the SYCL kernels
    recognize_text[(1,), (1,)](image_buffer, text_buffer)
    convert_to_speech[(1,), (1,)](text_buffer, speech_buffer)

    # Retrieve results from SYCL buffers
    text = text_buffer.to_host()[0]
    speech = speech_buffer.to_host()[0]

    if speech:
        return jsonify({'text': text})
    else:
        return jsonify({'text': 'Speech conversion failed.'})

@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
