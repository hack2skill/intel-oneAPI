# intel-oneAPI

#### Team Name - Chhota Bheem
#### Problem Statement - Object Detection For Autonomous Vehicles
#### Team Leader Email - rshrjacharya@gmail.com

## A Brief of the Prototype:
| Description | Diagram |
| :--- | :---: |
| The prototype presents the fastest possible implementation for custom object detection using the cutting-edge YOLOv8m model. This state-of-the-art model is specifically trained to detect pedestrians, vehicles, traffic signs, and traffic signals in real-world images, encompassing a wide range of weather conditions, lighting conditions, and road environments. To achieve exceptional speed and efficiency, the prototype harnesses the power of Intel Distribution for Python, Intel Optimization for TensorFlow, Intel Optimization for PyTorch, and Intel Neural Compressor from Intel AI Kit. These optimized tools significantly accelerate the pipeline's execution, resulting in unparalleled performance. In addition, the prototype incorporates post-training quantization techniques to convert the model's 32-bit float parameter data into highly efficient 8-bit fixed representations. This transformation enables the generation of a tflite model that is not only compatible with the Edge TPU but also maximizes the utilization of the available resources on Coral hardware. In summary, this prototype stands as the pinnacle of speed and efficiency, utilizing the state-of-the-art YOLOv8m model along with Intel's optimization tools and post-training quantization. The result is an ultra-fast and accurate object detection solution capable of handling real-world scenarios and optimized for deployment on Edge TPU and Coral hardware. | ![](https://raw.githubusercontent.com/rishiraj/intel-oneAPI/main/runs/detect/train/weights/best_saved_model/best_full_integer_quant_edgetpu.svg) |

![](https://raw.githubusercontent.com/rishiraj/intel-oneAPI/main/wandb/model.png)
Speed in milliseconds - lower is better. Upto 61.72% faster with Intel optimizations.

![](https://raw.githubusercontent.com/rishiraj/intel-oneAPI/main/wandb/metrics.png)
Metrics in fraction - higher is better.


## Tech Stack:
* Intel® AI Analytics Toolkit:
  * Intel® Distribution for Python (intelpython3_full -c intel)
  * Intel® Neural Compressor (neural-compressor -c intel)
  * Intel® Optimization for PyTorch (intel-aikit-pytorch -c intel)
  * Intel® Optimization for TensorFlow (intel-aikit-tensorflow -c intel)
* pytorch torchvision pytorch-cuda=11.7 -c pytorch -c nvidia

## Step-by-Step Code Execution Instructions:
```python
!git clone https://github.com/rishiraj/intel-oneAPI.git
!conda env create -f environment.yml # Installs Intel AIKit packages
```

### Inference:
```python
!pip install -q ultralytics
from ultralytics import YOLO
```
| If you want to run base model without any accelerator: | If you're using a CPU, use the following instead for up to 3x CPU speedup: | If you're using a GPU, use the following instead for up to 5x GPU speedup: | If you're using an Edge TPU, use the following instead for up to 10x TPU speedup: |
| :--- | :--- | :--- | :--- |
| `model = YOLO('rishiraj/intel-oneAPI/runs/detect/train/weights/best.pt')` | `model = YOLO('rishiraj/intel-oneAPI/runs/detect/train/weights/best.onnx')` | `model = YOLO('rishiraj/intel-oneAPI/runs/detect/train/weights/best.engine')` | `model = YOLO('rishiraj/intel-oneAPI/runs/detect/train/weights/best_saved_model/best_full_integer_quant_edgetpu.tflite')` |

| If you're running on a local machine / VM: | If you're running on a Google Colab notebook: |
| :--- | :--- |
| `import cv2` | `from google.colab.patches import cv2_imshow` |
| `cv2.imshow("result", model(img)[0].plot())` | `cv2_imshow(model(img)[0].plot())` |

### Training:
Run [train.ipynb](./train.ipynb) followed by [export.ipynb](./export.ipynb) to save trained model in format of choice.

## What I Learned:
Write about the biggest learning you had while developing the prototype
