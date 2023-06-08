# intel-oneAPI

#### Team Name -Team Xion
#### Problem Statement - Object Detection in Autonomous Vehicles
#### Team Leader Email -sarthakjoshisj93@gmail.com

## A Brief of the Prototype:
  -Developed a road sign detection model using the oneAPI framework in conjunction with the openVINO toolkit. 
  -Leveraged the oneAPI libraries and tools for efficient implementation and optimization. 
  -Utilized a dataset containing German road sign images for training and evaluation. 
  -Trained a deep learning model SSD using the dataset within the oneAPI framework. 
  -Fine-tuned the model to improve its accuracy in detecting Indian road signs. 
  -Converted the trained model to the OpenVINO Intermediate Representation (IR) format for deployment. Utilized openVINO's inference engine to perform real-time    road sign detection on different hardware platforms. 
  -Achieved high accuracy and real-time performance in road sign detection tasks using the combined power of the oneAPI framework and OpenVINO toolkit, showcasing their synergy in computer vision applications.
  
## Tech Stack: 
   * Intel SYCL/C++ Library
   * Intel Distribution for Python
   * openVINO
   * Visual Studio Code
   * Python 3.11
   * Intel DevCloud Platform
   
## Step-by-Step Code Execution Instructions:
   # Step 1: Install Required Libraries

- Make sure you have Python installed on your system.
- Install the necessary libraries, such as OpenCV, openVINO, and os, using pip or conda.

# Step 2: Gather and Preprocess Data

- Collect or create a dataset for training your object detection model.
- Annotate the dataset by labeling the objects of interest with bounding boxes.
- Split the dataset into training and testing sets.

# Step 3: Choose a Pre-Trained Model

- Select a pre-trained object detection model that suits your requirements.

# Step 4: Fine-tune the Model

- Load the pre-trained model weights.
- Replace the classification head with a new head suitable for your specific objects.
- Freeze the initial layers to retain the pre-trained weights.
- Train the model using the annotated training dataset.
- Adjust hyperparameters, such as learning rate and batch size, to optimize performance.

# Step 5: Evaluate the Model

- Evaluate the performance of your trained model using the testing dataset.
- Measure metrics like precision, recall, and average precision to assess the model's accuracy.

# Step 6: Implement Object Detection

- Use the trained model to perform object detection on new images or videos.
- Preprocess the input by resizing, normalizing, and converting it to the appropriate format.
- Pass the preprocessed input through the model to obtain predicted bounding boxes and class labels.
- Apply non-maximum suppression to remove redundant overlapping bounding boxes.
- Visualize the detected objects by drawing bounding boxes and labels on the input image or video.

  
## What I Learned:
   In this road sign detection project utilizing oneAPI, our team gained significant insights and expertise in several key areas. We developed a strong proficiency in oneAPI integration, computer vision techniques, dataset collection and annotation, model training, performance evaluation, error analysis, and real-world application considerations. This project honed our skills in handling oneAPIs effectively, implementing advanced computer vision algorithms, optimizing models, and addressing practical challenges. Overall, the project enriched our knowledge and capabilities in road sign detection, empowering us to tackle complex computer vision tasks with confidence and expertise.
