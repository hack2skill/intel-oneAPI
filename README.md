# intel-oneAPI

#### Team Name - Ai Artistss
#### Problem Statement - Object Detection For Autonomous Vehicles
#### Team Leader Email - riddhishwar.s2020@vitstudent.ac.in

## 📜 A Brief of the Prototype:
- Our prototype's real-time object detection and distance recognition features are meant to make self-driving cars safer and more efficient. By leveraging the power of Intel technologies and frameworks, we've created a robust system that combines advanced computer vision algorithms and deep learning models.Intel AI Analytics Toolkit, featuring optimised deep learning frameworks like PyTorch and TensorFlow, powers the prototype. Intel-optimized libraries like oneDNN and oneDAL were used to train and infer deep learning models. This helps us locate items around the car.

![Screenshot 2023-06-08 224156](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/76ffb3f4-7977-4bc2-8e0d-6826b45aff5e)
![Screenshot 2023-06-08 224156](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/e0a0869a-2830-43f2-89c5-336e32ac5a35)

## Architecture Diagram: 
![Screenshot 2023-06-09 181317](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/93c796c8-9a13-4a41-ac06-c343c20f3ebf)

## Flow Diagram:
![Screenshot 2023-06-09 181606](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/8c6dc9d9-6955-4908-b164-c00728b7738f)

## 🍞 Folder Structure
```bash
|-client                            #client side folder (frontend code)
|  public
|     --
|  src                              #building the source code
|     assests
|     components                    #building the business component for our website
|     App.js                        #Root folder for the division for each components
|     index.css
|     index.js
|  package.json
|  package-lock.json
|
|-dataset
|     export
|        -images                    #containing the images for training,validating and testing our model
|        -labels                    #contains the equivalent format yolo format for each images
|     data.yaml
|
|-yolov5
|     classify
|        ...
|     data
|        ...
|        custom_dataset.yaml        #this is the .yaml file for training our model
|        ...
|     ...
|     requirements.txt              #contains all the necessary packages
|     ...
```


## 📜 Tech Stack: 
   List Down all technologies used to Build the prototype **Clearly mentioning Intel® AI Analytics Toolkits, it's libraries and the SYCL/DCP++ Libraries used**
   ![Screenshot 2023-06-09 182951](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/08f722e9-7637-4a44-877a-b496d5fde92f)
   ![qwe](https://github.com/Senthil-Riddhish/Ai-Artistss/assets/82893678/de88cc7b-d827-4601-909e-dc07e47d3253)
## Step-by-Step Code Execution Instructions:
  This Section must contain set of instructions required to clone and run the prototype, so that it can be tested and deeply analysed
  ## Installation


  Clone repo and install [requirements.txt](https://github.com/Senthil-Riddhish/Ai-Artistss/blob/main/yolov5/requirements.txt) in a
   [**Python>=3.7.0**](https://www.python.org/) environment, including
   [**PyTorch>=1.7**](https://pytorch.org/get-started/locally/).

   ```bash
   git clone https://github.com/ultralytics/yolov5  # clone
   cd yolov5
   pip install -r requirements.txt  # install
   ```
   <summary>Training</summary>

The commands below reproduce YOLOv5 [COCO](https://github.com/ultralytics/yolov5/blob/master/data/scripts/get_coco.sh)
results. [Models](https://github.com/ultralytics/yolov5/tree/master/models)
and [datasets](https://github.com/ultralytics/yolov5/tree/master/data) download automatically from the latest
YOLOv5 [release](https://github.com/ultralytics/yolov5/releases). Training times for YOLOv5n/s/m/l/x are
1/2/4/6/8 days on a V100 GPU ([Multi-GPU](https://docs.ultralytics.com/yolov5/tutorials/multi_gpu_training) times faster). Use the
largest `--batch-size` possible, or pass `--batch-size -1` for
YOLOv5 [AutoBatch](https://github.com/ultralytics/yolov5/pull/5092). Batch sizes shown for V100-16GB.
### Just get into the yolov5 folder and execute this commnd for training the model
```bash
python train.py --data custom_dataset.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
                                                                 yolov5s                    64
                                                                 yolov5m                    40
                                                                 yolov5l                    24
                                                                 yolov5x                    16
```
## What I Learned:
   Write about the biggest learning you had while developing the prototype
