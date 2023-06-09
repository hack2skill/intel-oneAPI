# intel-oneAPI

#### Team Name - Meteors
#### Problem Statement - Object Detection For Autonomous Vehicles
#### Team Leader Email - padmakumarr21cb@psnacet.edu.in

## A Brief of the Prototype:

The prototype developed for this project is a state-of-the-art autonomous vehicle object detection system. It integrates deep learning models, specifically Faster R-CNN (MobileNetV3-Large) and YOLOv5, to accurately identify and classify various objects, including vehicles, traffic signals, traffic signs, and pedestrians. The prototype's primary objective is to enhance the safety and efficiency of autonomous vehicles by providing real-time and reliable object detection capabilities.

The prototype consists of two distinct frameworks, each employing a different deep learning model. It undergoes a comprehensive benchmarking process, evaluating the performance of the models under different conditions. To further optimize the models, Intel oneAPI libraries, such as Intel oneDNN leveraged. These libraries enhance the efficiency and processing speed of the models, resulting in a remarkable 50% improvement in inference time compared to running the models without the Intel oneAPI libraries. The prototype showcases the effectiveness of integrating deep learning models with Intel oneAPI libraries in achieving highly accurate and efficient object detection for autonomous vehicles.
  
  ![Record video feeds (7)](https://github.com/rppadmakumar3/oneAPI_ObjectDetection/assets/116913142/26734649-6e74-4ba4-8a56-66ecfcca055a)

  
## Tech Stack: 
   ### Python
   Python is the primary programming language used to write the code for the object detection system.
   
   ### PyTorch
   PyTorch is the deep learning framework utilized to build the object detection models. It offers high-level abstractions, making it easier to develop, train,      and fine-tune deep learning models.
   
   ### IPEX (Intel Extension for PyTorch)
   IPEX is used to optimize the performance of the PyTorch models. It is an Intel oneAPI library that provides additional optimizations for PyTorch, enhancing        their efficiency and speed during the inference process.
   
   ### Streamlit
  Streamlit is used to develop the web application interface for the object detection system. It allows for easy creation of interactive and data-driven             applications, enabling users to upload images or videos for object detection.
   
   ### Jupyter Notebook
   Jupyter Notebook provides an interactive environment for analyzing and exploring the object detection system.It allows for in-depth analysis of the models,        evaluation of performance metrics, and visualization of results.
   
   ### Intel DevCloud Platform
   The Intel DevCloud Platform provides a cloud-based environment for testing and evaluating the prototype.It offers access to Intel hardware resources and          accelerators, allowing for performance testing and optimization of the object detection system.
   
## Step-by-Step Code Execution Instructions:

We used 2 Models such as YOLOv5 and FasterRCNN architecture. Each model has 2 Main folders, that are Benchmarking and Training. In the `Training` folder we uploaded the code used in training phase. In the `Benchmarking` folder we uploaded the code used in Inference stage. Also we have separate folder for With oneAPI using and Without using. We test two types of image. That are Day time Captured and Night Time Captured.

## Clone the repository
```
git clone https://github.com/rppadmakumar3/oneAPI_ObjectDetection
```
# Web Application

# Object Detection for Autonomous Vehicles
A web interface for real-time object detection inference using streamlit. It supports CPU and GPU inference.


## Features
- Supports:
  - Custom Classes
  - Changing Confidence
  - Changing input/frame size for videos

## To run the Web Application
```
cd WebApp
```


## How to run
After cloning the repo:
1. Install requirements
   - `pip install -r requirements.txt`
2. Add sample images to `data/sample_images`
3. Add sample video to `data/sample_videos` and call it `sample.mp4` or change name in the code.
4. Add the model file to `models/` and change `cfg_model_path` to its path.
```bash
streamlit run app.py
```

## Results

### YOLOv5 Results
![YOLOv5_DayTime_Benchmark](https://github.com/rppadmakumar3/oneAPI_ObjectDetection/assets/116913142/a8deda37-52af-42ca-8509-212b84fb220b)

### FasterRCNN Results
![FasterRCNN_NightTime_Benchmark](https://github.com/rppadmakumar3/oneAPI_ObjectDetection/assets/116913142/b6d3829a-4806-46d1-8d86-00ae60df742f)



Medium Article Link: [Optimizing Object Detection for Autonomous Vehicles](https://medium.com/@creatorrp3010/optimizing-object-detection-for-autonomous-vehicles-leveraging-intel-oneapi-libraries-for-enhanced-3f7341f675d5)
Demo Video: [Object Detection for Autonomous Vecihles](https://www.youtube.com/watch?v=dWaTq5gzsvU)

## What I Learned:

Deep Learning Model Selection: Through this project, I gained insights into different deep learning models for object detection, specifically comparing Faster R-CNN (MobileNetV3-Large) and YOLOv5. I learned how to choose the most suitable model based on factors like accuracy, speed, and resource efficiency.

Integration of Intel oneAPI Libraries: I learned how to leverage Intel oneAPI libraries, such as Intel oneDNN and Intel IPEX, to optimize the performance of deep learning models. By incorporating these libraries, I experienced significant improvements in inference time and overall model efficiency.

Web Application Development with Flask: Building the user interface using Flask introduced me to the fundamentals of web application development. I learned how to handle routing, requests, and templating, enabling seamless interactions with the object detection system.

Benchmarking and Performance Evaluation: Throughout the project, I gained valuable experience in benchmarking and evaluating the performance of deep learning models. By comparing results with and without Intel oneAPI libraries, I developed a deeper understanding of the impact of optimization techniques on model inference time.

Real-world Scenario Considerations: Working with images and videos captured in different lighting conditions (daytime and nighttime) allowed me to assess the robustness of the models in real-world scenarios. I learned the importance of testing and optimizing models for various environmental factors to ensure reliable performance in different situations.

Overall, this project provided me with hands-on experience in deep learning model selection, integration of optimization libraries, web application development, benchmarking, and considering real-world scenarios. It enhanced my knowledge of object detection techniques and the practical aspects of deploying such systems in autonomous vehicles.
