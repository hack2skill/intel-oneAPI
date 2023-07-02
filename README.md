# intel-oneAPI

#### Team Name - SneakyTurtle <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/f7ee32ba-d85e-4ab3-8731-b6701d94b313" height = "50px">

#### Problem Statement - Object Detection For Autonomous Vehicles <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/549af82b-79e6-436a-b067-2e83641a9095" height = "50px">
#### Team Leader Email - shreyashmohadikar@gmail.com




## <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/80522c5e-f814-4c3d-906a-e5518ccdd150" height = "50px" > A Brief of the Prototype:
  
  
  <img src ="https://media.giphy.com/media/dqQxplKANtn8c/giphy.gif" height = "250" width = "100%"/>
  
  
This repository contains the code and resources for an advanced object detection model for autonomous vehicles. The Prototpe is designed to excel in extreme weather conditions like fog and snow, thereby improving the safety and reliability of autonomous driving systems.

### Dataset Acquisition
The dataset used in this project was obtained from Roboflow, a platform for computer vision data management. The dataset can be accessed using the following link: [Roboflow - Self-driving Car Object Detection](https://public.roboflow.com/object-detection/self-driving-car)


### Heatmap of annotations
<p> 
  <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/27cb8e80-2b6d-46d7-8490-7a7299c59e22">
</p>

The FOV of the car is located around the centre of the image in most of the times. The above image represents the same, where the obstacles such as cars and pedestrians are located at the centre of the image, hence we have a denser heatmap over there.


### Data Preprocessing
To prepare the dataset for training, we utilized the preprocessing capabilities offered by Roboflow. The following preprocessing steps were applied to the images:

- Auto-orientation of pixel data, including EXIF-orientation stripping.
- Resizing the images to a resolution of 480x480 pixels using a stretch method.
- Random brightness adjustment of the images within a range of -50% to +50%.
- Random brightness adjustment of the images within a range of -25% to +25%.
- Random Gaussian blur with a variance between 0 and 2 pixels.
- The image noise to 10% of the pixels in the images.


Before Preprocessing             |  After Preprocessing 
:-------------------------:|:-------------------------:
![image](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/a702af3b-eb31-4df4-acd7-f9de9e76232e)| ![](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/65ea01af-1d05-4dce-a0a1-a578d9177946)
I->|  ![](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/ea11af47-5d7b-4ce8-8290-95e491653cad)






### Model Training
After preprocessing the dataset, we employed the DETR (Detection Transformer) transfer learning technique to train our advanced object detection model. By leveraging this state-of-the-art approach, we aimed to enhance the model's ability to accurately detect and classify objects in real-time, even in challenging weather conditions.  
Using Intel's OneAPI Pytorch Optimization Framework(IPEX) and neural compressor on Intel DevCloud, the model training has been optimized. The training and inference time have decreased drastically facilitating faster model usage and deployment. 

![image](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/98dec7de-6785-4d11-aa45-1ad35c2cd64f)          |  ![image](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/a7757420-181b-4277-b7c0-2e0b19b095fc)
:-------------------------:|:-------------------------:





### Deployment
For the deployment of the trained prototype, we used Flask. We developed a web application that provides an intuitive interface for users to use the prototype. The Flask app allows users to upload images for object detection. The detected objects are then visualized and displayed to the user, providing valuable insights and enhancing the capabilities of autonomous driving systems.




<p align = "center" > 
  <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/7c5c24ad-3f94-4c5b-82bc-17cc2f95afd1">
</p>


### Process Flow Diagram
![image](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/60a6fbfc-a7a9-4436-aba8-25d6ffd8fb31)



### Architecture Diagram
![image](https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/4ae5024a-068c-42aa-abca-6adfab25bb46)




### Repository Structure
- `Deployment/`: You can find the deployment of the prototype.
- `notebooks/`: Jupyter notebooks showcasing the data preprocessing, model training, and evaluation processes.
- `README.md`: The file you are currently reading, providing an overview of the project.


<div id="bringHere"></div>

### Note: Please download the model file from [here](https://drive.google.com/file/d/1vxFshXVYC76bIlvoaqJlnHqjsrhv7iTA/view?usp=sharing) and save it in the `Deployment/` repository as `vehicle_det.pth` before use.
  
  

##  <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/51de0cd9-f6e8-43ce-bb09-baccd71c0447" height = "50px">  Tech Stack: 
1. Roboflow: For image input and preprocessing.
1. OneDAN: For data analysis of images and drawing conclusions.
1. OneDNN: for framework optimization.
1. OneVPL: video processing tasks.
1. Google Colaboratory: For coding and effective communication between team members.
1. Pytorch framework
1. Flask: For deployment of the solution.


![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Colab](https://img.shields.io/badge/google%20colab-%040404.svg?style=for-the-badge&logo=googlecolab&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
and more..

## <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/8d918e92-7fa3-4218-80b9-d47a0c0e7bcb" height = "50px"> Step-by-Step Code Execution Instructions:
  #### To clone and run the prototype use the following instructions:
  1. Open up a bash terminal(Linux) or Command Prompt(Windows)
  2. Cone the repository with the code: `git clone https://github.com/SneakyTurtIe/intel-oneAPI.git`
  4. Change the working directory to the deployment directory: `cd intel-oneAPI/Deployment`
  5. Install the model file as mentioned <a href="#bringHere">here</a>.
  6. Install the requirements of the project with `pip install -r requirements.txt`
  7. Run the deployment on localhost using the command: `python app.py`

<p align="center">
  Your prototype should be running at localhost:5000 <br>
  <img src = "https://media.giphy.com/media/JqDeI2yjpSRgdh35oe/giphy.gif" height = "250"/>
</p>

## What I Learned:
During the course of our project in object detection for autonomous vehicles, we have gained valuable insights and experiences. Here are the elaborations and additional points:

Limitations of existing models: We have identified several limitations in existing object detection models, particularly in extreme weather conditions such as fog, mist, and camouflage. These conditions can significantly affect the accuracy and reliability of object detection algorithms, making it essential to address these challenges.

Specialized models for extreme weather: Recognizing the limitations, we have emphasized the importance of developing specialized models specifically tailored for extreme weather conditions. These models incorporate advanced techniques and algorithms that can handle the challenges posed by weather-related factors, enabling more accurate and robust object detection.

Data augmentation for weather conditions: To tackle the limitations caused by extreme weather, we performed data augmentation techniques. By augmenting the dataset to resemble various weather conditions, such as fog and mist, we aimed to train the object detection models to be more resilient and adaptable in adverse weather scenarios.

Pre-processing steps: As part of the data preparation, we applied pre-processing steps to each image. These steps included auto-orientation of pixel data with EXIF-orientation stripping and resizing the images to a standardized size of 480x480 pixels, allowing consistent input for the object detection models.

Augmentation techniques: To create diverse variations of each source image, we employed augmentation techniques. This involved randomly adjusting the brightness of the images within a range of -25% to +25%, applying random Gaussian blur with a range of 0 to 2 pixels, and introducing salt and pepper noise to 10% of the pixels. These augmentations aimed to increase the variability of the dataset and improve the model's generalization capabilities.

Leveraging Intel's oneAPI OneDNN: Throughout our project, we explored the capabilities of Intel's oneAPI OneDNN tool. By utilizing this deep neural network tool, we were able to optimize and accelerate the performance of our object detection code. Leveraging hardware accelerators and parallel computing, we achieved improved efficiency and speed in our models.

Overall, our project focused on addressing the limitations of existing object detection models in extreme weather conditions. Through specialized model development, data augmentation, and the use of advanced tools like Intel's oneAPI OneDNN, we aimed to improve the accuracy, reliability, and robustness of object detection for autonomous vehicles in challenging weather scenarios.




