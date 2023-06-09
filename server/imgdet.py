from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import os
import tensorflow as tf


# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

image = "uploads/1.jpg"
image = tf.image.resize(image, [224, 224])
image = tf.cast(image, tf.float32) / 255.0
image = np.expand_dims(image, axis=0)

# Set the input tensor with the preprocessed image
interpreter.set_tensor(input_details[0]['index'], image)

# Run the inference
interpreter.invoke()

# Get the output tensor and convert it to a probability distribution
output_tensor = interpreter.get_tensor(output_details[0]['index'])
probabilities = tf.nn.softmax(output_tensor).numpy()

# Get the predicted class label
predicted_class = np.argmax(probabilities)

print(predicted_class, probabilities[0])
