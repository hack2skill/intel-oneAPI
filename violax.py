
import cv2
import numpy as np
from daal4py import dnn, engine, batch_normalization_training, split, convolution2d, fullyconnected, relu, \
    loss_cross_entropy, softmax
from openvino.inference_engine import IECore

# Load the model and configuration files
model_xml = "path/to/model.xml"
model_bin = "path/to/model.bin"
model_classes = "path/to/model.classes"

# Load the class labels
with open(model_classes, 'r') as f:
    classes = f.read().splitlines()

# Load the input image
image = cv2.imread("path/to/image.jpg")

# Preprocess the input image
input_image = cv2.resize(image, (416, 416))
input_image = input_image.transpose((2, 0, 1))
input_image = input_image[np.newaxis, :]

# Create the computation graph using oneDNN
g = engine(graph_kind='direct')

input_layout = dnn.layout((1, 3, 416, 416))
input_memory = engine.memory(input_layout, 'input')
input_memory.allocate()

net = dnn.network(g, input_layout)
input_prim = dnn.input(g, input_memory)
net.add_data(input_prim)

conv1_weights = engine.memory(batch_normalization_training.cnn2d_weights_layout(input_layout, 32), 'weights')
conv1_biases = engine.memory(batch_normalization_training.cnn2d_biases_layout(input_layout, 32), 'biases')

conv1_memory = engine.memory(batch_normalization_training.cnn2d_layout(input_layout, 32), 'conv1')
conv1_memory.allocate()
conv1 = convolution2d(g, input_prim, conv1_weights, conv1_biases, conv1_memory)

relu1_memory = engine.memory(conv1_memory.get_primitive_desc().desc(), 'relu1')
relu1_memory.allocate()
relu1 = relu(g, conv1_memory, relu1_memory)

split1_memory = engine.memory(relu1_memory.get_primitive_desc().desc(), 'split1')
split1_memory.allocate()
split1 = split(g, relu1_memory, split1_memory)

# ... Add more layers as required for your model

# Execute the graph using oneDAL
input_memory.set_data(input_image)

g.compute()

# Get the output from the last layer
output_memory = net.get_output_memory()
output_data = np.array(output_memory.get_data())

# Process the output detections
objects = []
for detection in output_data:
    scores = detection[5:]
    class_id = np.argmax(scores)
    confidence = scores[class_id]

    if confidence > 0.5:
        label = classes[class_id]
        xmin = int(detection[3] * image.shape[1])
        ymin = int(detection[4] * image.shape[0])
        xmax = int(detection[5] * image.shape[1])
        ymax = int(detection[6] * image.shape[0])
        objects.append((label, confidence, (xmin, ymin, xmax, ymax)))

# Draw bounding boxes on the image
for label, confidence, (xmin, ymin, xmax, ymax) in objects:
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    cv2.putText(image, f"{label}: {confidence:.2f}", (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding boxes
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()