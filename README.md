# intel-oneAPI

#### Team Name - SneakyTurtle <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/f7ee32ba-d85e-4ab3-8731-b6701d94b313" height = "50px">

#### Problem Statement - Object Detection For Autonomous Vehicles <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/549af82b-79e6-436a-b067-2e83641a9095" height = "50px">
#### Team Leader Email - shreyashmohadikar@gmail.com




## <img src = "https://github.com/SneakyTurtIe/intel-oneAPI/assets/59119736/80522c5e-f814-4c3d-906a-e5518ccdd150" height = "50px" > A Brief of the Prototype:
  
  
  <img src ="https://media.giphy.com/media/dqQxplKANtn8c/giphy.gif" height = "250" width = "100%"/>
  
  
This repository contains the code and resources for an advanced object detection model for autonomous vehicles. The Prototpe is designed to excel in extreme weather conditions like fog and snow, thereby improving the safety and reliability of autonomous driving systems.

### Dataset Acquisition
The dataset used in this project was obtained from Roboflow, a platform for computer vision data management. The dataset can be accessed using the following link: [Roboflow - Self-driving Car Object Detection](https://public.roboflow.com/object-detection/self-driving-car)

### Data Preprocessing
To prepare the dataset for training, we utilized the preprocessing capabilities offered by Roboflow. The following preprocessing steps were applied to the images:

- Auto-orientation of pixel data, including EXIF-orientation stripping.
- Resizing the images to a resolution of 640x640 pixels using a stretch method.
- Random brightness adjustment of the images within a range of -26% to +26%.
- Random Gaussian blur with a variance between 0 and 2 pixels.
- The application of salt and pepper noise to 2% of the pixels in the images.

### Model Training
After preprocessing the dataset, we employed the DETR (Detection Transformer) transfer learning technique to train our advanced object detection model. By leveraging this state-of-the-art approach, we aimed to enhance the model's ability to accurately detect and classify objects in real-time, even in challenging weather conditions.

### Deployment
For the deployment of the trained prototype, we used Flask. We developed a web application that provides an intuitive interface for users to use the prototype. The Flask app allows users to upload images for object detection. The detected objects are then visualized and displayed to the user, providing valuable insights and enhancing the capabilities of autonomous driving systems.

### Repository Structure
- `Deployment/`: You can find the deployment of the prototype.
- `notebooks/`: Jupyter notebooks showcasing the data preprocessing, model training, and evaluation processes.
- `README.md`: The file you are currently reading, providing an overview of the project.



  
  

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
  3. Change the working directory to the deployment directory: `cd intel-oneAPI/Deployment`
  4. Install the requirements of the project with `pip install -r requirements.txt`
  5. Run the deployment on localhost using the command: `python app.py`

<p align="center">
  Your prototype should be running at localhost:5000 <br>
  <img src = "https://media.giphy.com/media/JqDeI2yjpSRgdh35oe/giphy.gif" height = "250"/>
</p>

## What I Learned:
Throughout the course of this project, we gained valuable insights and knowledge in the field of object detection for autonomous vehicles. We learnt about the limitations of existing models in extreme weather conditions and the importance of developing specialized models for such scenarios. Additionally, we acquired hands-on experience in leveraging the DETR transfer learning technique to create an advanced object detection model. Furthermore, we explored the capabilities of Intel's oneAPI OneDNN tool and discovered its effectiveness in optimizing and accelerating the performance of the code.





