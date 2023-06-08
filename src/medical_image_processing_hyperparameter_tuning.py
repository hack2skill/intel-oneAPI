import os
import sys
import argparse
from pathlib import Path
import time
import warnings
from cv2 import cv2
import numpy as np
from openvino.inference_engine import IECore
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# Define variables with predefined values
INPUT_IMAGE_SIZE = (300, 300)
NUM_OUTPUT_CLASSES = 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--datadir", type=str, default="./data/chest_xray", help="Provide the exact data path")
    args = parser.parse_args()

data_dir_path = args.datadir
data_dir = Path("./data/chest_xray/train/NORMAL") and Path("./data/chest_xray/train/PNEUMONIA")
data_files = []
for p in data_dir.glob("**/*"):
    if p.suffix in (".jpeg"):
        data_files.append(p)
try:
    if len(data_files) == 0:
        logger.info("Unable to find Images")
except:
    logger.info('Images not found or format not supported, execution failed')
    sys.exit()


# Define the method to create a path list where data needs to be read
def create_path_list(abspath="None"):
    pathlist = []
    for (root, dirs, files) in os.walk(abspath):
        for subdir in dirs:
            for imgpath in os.listdir(os.path.join(abspath, subdir)):
                if imgpath.endswith('.jpeg'):
                    img_append = os.path.join(abspath, subdir, imgpath)
                    pathlist.append(img_append)
        break
    return pathlist


# Enter the paths of valid, training & testing just to make sure all the paths are correct
ABS_VAL_PATH = os.path.join(data_dir_path, "val")
logger.info("ABS_VAL_PATH is ============================================>%s", ABS_VAL_PATH)
ABS_TRAIN_PATH = os.path.join(data_dir_path, "train")
logger.info("ABS_TRAIN_PATH is ============================================>%s", ABS_TRAIN_PATH)
ABS_TEST_PATH = os.path.join(data_dir_path, "test")
logger.info("ABS_TEST_PATH is ============================================>%s", ABS_TEST_PATH)

# Checking the train dataset
if os.path.isdir(ABS_VAL_PATH) and os.path.isdir(ABS_TRAIN_PATH) and os.path.isdir(ABS_TEST_PATH):
    logger.info("Data paths exist, executing the program")
else:
    logger.info("Valid path not found")
    sys.exit()


# Read the image from the path defined above
def read_image(batch_size=4, LAST_INDEX=2, pathlist=None):
    x_batch, y_batch = [], []
    for imagepath in pathlist[LAST_INDEX:LAST_INDEX+batch_size]:
        image = cv2.imread(imagepath)
        image = cv2.resize(image, dsize=INPUT_IMAGE_SIZE)
        image = image / 255.0
        if imagepath.split('/')[-2] == 'NORMAL':
            y = np.array([0, 1])
        else:
            y = np.array([1, 0])
        x_batch.append(image)
        y_batch.append(y)
    x_batch_train = np.stack(x_batch, axis=0)
    y_batch_train = np.stack(y_batch, axis=0)
    return x_batch_train, y_batch_train


# Placeholder code to check if Image is loading properly
train_list = create_path_list(ABS_TRAIN_PATH)
train_images, train_labels = read_image(batch_size=4, LAST_INDEX=0, pathlist=train_list)

# Initialize the OpenVINO Inference Engine Core
ie = IECore()

# Load the IR files (XML and BIN) for the model
model_xml = 'model.xml'
model_bin = 'model.bin'
net = ie.read_network(model=model_xml, weights=model_bin)

# Get the input and output node names
input_blob = next(iter(net.input_info))
output_blob = next(iter(net.outputs))

# Load the network onto the Intel hardware
exec_net = ie.load_network(network=net, device_name='CPU')

# Prepare the input image for inference
input_data = np.expand_dims(train_images, axis=0)

# Perform inference
start_time = time.time()
outputs = exec_net.infer(inputs={input_blob: input_data})
end_time = time.time()
inference_time = end_time - start_time

# Process the outputs
output_data = outputs[output_blob]
predicted_classes = np.argmax(output_data, axis=1)

# Print the predicted classes
for predicted_class in predicted_classes:
    print(f"Predicted class: {predicted_class}")

# Print the inference time
print(f"Inference time: {inference_time} seconds")
