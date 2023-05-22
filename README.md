# intel-oneAPI

#### Team Name - Chhota Bheem
#### Problem Statement - Object Detection For Autonomous Vehicles
#### Team Leader Email - rshrjacharya@gmail.com

## A Brief of the Prototype:
The prototype presents the fastest possible implementation for custom object detection using the cutting-edge YOLOv8m model. This state-of-the-art model is specifically trained to detect pedestrians, vehicles, traffic signs, and traffic signals in real-world images, encompassing a wide range of weather conditions, lighting conditions, and road environments.

To achieve exceptional speed and efficiency, the prototype harnesses the power of Intel Distribution for Python, Intel Optimization for TensorFlow, Intel Optimization for PyTorch, and Intel Neural Compressor from Intel AI Kit. These optimized tools significantly accelerate the pipeline's execution, resulting in unparalleled performance.

In addition, the prototype incorporates post-training quantization techniques to convert the model's 32-bit float parameter data into highly efficient 8-bit fixed representations. This transformation enables the generation of a tflite model that is not only compatible with the Edge TPU but also maximizes the utilization of the available resources on Coral hardware.

In summary, this prototype stands as the pinnacle of speed and efficiency, utilizing the state-of-the-art YOLOv8m model along with Intel's optimization tools and post-training quantization. The result is an ultra-fast and accurate object detection solution capable of handling real-world scenarios and optimized for deployment on Edge TPU and Coral hardware.

## Tech Stack:
* Intel® AI Analytics Toolkit:
  * Intel® Distribution for Python (intelpython3_full -c intel)
  * Intel® Neural Compressor (neural-compressor -c intel)
  * Intel® Optimization for PyTorch (intel-aikit-pytorch -c intel)
  * Intel® Optimization for TensorFlow (intel-aikit-tensorflow -c intel)
* pytorch torchvision pytorch-cuda=11.7 -c pytorch -c nvidia

## Step-by-Step Code Execution Instructions:
This Section must contain set of instructions required to clone and run the prototype, so that it can be tested and deeply analysed

## What I Learned:
Write about the biggest learning you had while developing the prototype
