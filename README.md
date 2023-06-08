# intel-oneAPI

#### Team Name -Team Xion
#### Problem Statement - Object Detection in Autonomous Vehicles
#### Team Leader Email - sarthakjoshisj93@gmail.com

## A Brief of the Prototype:
  #### Developed a road sign detection model using the oneAPI framework in conjunction with the openVINO toolkit. 
  ####  Leveraged the oneAPI libraries and tools for efficient implementation and optimization. 
  ####  Utilized a dataset containing German road sign images for training and evaluation. 
  ####  Trained a deep learning model SSD using the dataset within the oneAPI framework. 
  ####  Fine-tuned the model to improve its accuracy in detecting Indian road signs. 
  ####  Converted the trained model to the OpenVINO Intermediate Representation (IR) format for deployment. Utilized openVINO's inference engine to perform real-time    road sign detection on different hardware platforms. 
  ####  Achieved high accuracy and real-time performance in road sign detection tasks using the combined power of the oneAPI framework and OpenVINO toolkit, showcasing their synergy in computer vision applications.
  
  ### Diagram
  ![Diagram](https://github.com/Craniace/intel-oneAPI/assets/100042684/be5c1803-083c-4879-8cde-c2d4ec154092)


## Tech Stack: 
   * Intel SYCL/C++ Library
   * Intel Distribution for Python
   * openVINO for Python
   * Visual Studio Code
   * Python 3.11
   * Intel DevCloud Platform
   
## Step-by-Step Code Execution Instructions:
   ### Step 1: Install Required Libraries

- Make sure you have Python installed on your system.
- Install the necessary libraries, such as OpenCV, openVINO, and os, using pip or conda.

### Step 2: Gather and Preprocess Data

- Collect or create a dataset for training your object detection model.
- Annotate the dataset by labeling the objects of interest with bounding boxes.
- Split the dataset into training and testing sets.

### Step 3: Choose a Pre-Trained Model

- Select a pre-trained object detection model that suits your requirements.

### Step 4: Fine-tune the Model

- Load the pre-trained model weights.
- Replace the classification head with a new head suitable for your specific objects.
- Freeze the initial layers to retain the pre-trained weights.
- Train the model using the annotated training dataset.
- Adjust hyperparameters, such as learning rate and batch size, to optimize performance.

### Step 5: Evaluate the Model

- Evaluate the performance of your trained model using the testing dataset.
- Measure metrics like precision, recall, and average precision to assess the model's accuracy.

### Step 6: Implement Object Detection

- Use the trained model to perform object detection on new images or videos.
- Preprocess the input by resizing, normalizing, and converting it to the appropriate format.
- Pass the preprocessed input through the model to obtain predicted bounding boxes and class labels.
- Apply non-maximum suppression to remove redundant overlapping bounding boxes.
- Visualize the detected objects by drawing bounding boxes and labels on the input image or video.

  
## What I Learned:
 **Image processing and computer vision techniques:** Road sign detection often involves applying various image processing and computer vision algorithms to identify and locate signs within images or video streams. This includes techniques like image segmentation, feature extraction, and object detection.

**Data collection and preprocessing:** Gathering a diverse dataset of road sign images is crucial for training and evaluating the detection model. You would have learned how to collect and preprocess the data, including labeling the signs and handling data augmentation techniques.

**Model selection and training:** Choosing an appropriate model architecture for road sign detection and training it using the collected dataset. This involves understanding different deep learning models and their suitability for the task, selecting loss functions, and optimizing hyperparameters.

**Integration of oneAPI tools:** oneAPI provides a unified programming model for diverse hardware architectures. You would have learned how to leverage oneAPI tools, such as oneDNN (oneAPI Deep Neural Network Library) and oneVPL (oneAPI Video Processing Library), to optimize and accelerate the road sign detection pipeline on specific hardware platforms.

**Performance optimization:** Road sign detection often requires real-time or near real-time processing, especially in autonomous driving applications. You would have explored optimization techniques to improve the inference speed and efficiency of the detection model, such as model quantization, pruning, and parallelization.

**Evaluation and accuracy assessment:** Assessing the performance of the road sign detection model through evaluation metrics like precision, recall, and F1 score. This helps measure the accuracy and effectiveness of the model in correctly identifying road signs.

**Deployment and integration:** Integrating the trained road sign detection model into larger systems or applications, such as autonomous vehicles or traffic management systems. This involves considering deployment requirements, performance constraints, and compatibility with existing software or hardware components.


