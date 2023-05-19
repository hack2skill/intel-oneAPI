# intel-oneAPI

#### Team Name - Error 404
#### Problem Statement -  Advance Object Detection in Python for Autonomous vehicle 
#### Team Leader Email - dhruvabhattacharya130102@gmail.com

## A Brief of the Prototype:
Object detection plays a crucial role in enabling autonomous vehicles to perceive and understand their surroundings. By accurately identifying and tracking objects in real-time, we enhance the safety, efficiency, and overall performance of autonomous driving systems.

SYCL/DPC++ libraries provide a powerful framework for high-performance computing and parallel programming. With their capabilities for heterogeneous computing, we can now harness the full potential of modern GPUs and accelerators to accelerate the object detection process significantly.

By utilizing SYCL/DPC++ libraries, we have created a Python-based solution that brings state-of-the-art object detection algorithms to the realm of autonomous vehicles. This solution combines the flexibility and ease of use of Python with the performance benefits of SYCL/DPC++ libraries, resulting in an efficient and robust system for object detection.

## Architectural Diagram of the Project
![Architect Diagram](https://user-images.githubusercontent.com/71749153/239616833-06e0983d-a007-4514-800c-b4effaf13ac2.png)

## Process Flow Diagram of the Project
![Process Flow](https://user-images.githubusercontent.com/71749153/239616264-1e6d5b65-b05d-4406-a37e-562616a3f45f.png)
  
## Tech Stack: 
In the context of advanced object detection, the Intel® AI Analytics Toolkits offer powerful features and libraries that facilitate the development and deployment of object detection      models. These libraries provide optimized algorithms and functions for tasks such as image preprocessing, feature extraction, and model training and inference.

Additionally, the tech stack incorporates the SYCL/DCP++ Libraries, which are specifically designed for heterogeneous computing environments. SYCL (pronounced "sickle") stands for "Single-source Heterogeneous Programming for OpenCL™," and it enables developers to write code once and target various devices, such as CPUs, GPUs, and FPGAs, with high performance and efficiency
   
## Step-by-Step Code Execution Instructions:

  # Step 1: Install Required Libraries

- Make sure you have Python installed on your system.
- Install the necessary libraries, such as OpenCV, TensorFlow, and Keras, using pip or conda.

# Step 2: Gather and Preprocess Data

- Collect or create a dataset for training your object detection model.
- Annotate the dataset by labeling the objects of interest with bounding boxes.
- Split the dataset into training and testing sets.

# Step 3: Choose a Pre-Trained Model

- Select a pre-trained object detection model that suits your requirements. Popular choices include YOLO (You Only Look Once), SSD (Single Shot MultiBox Detector), and Faster R-CNN (Region-     based Convolutional Neural Networks).

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

# Step 7: Fine-tune and Iterate

- Analyze the results and identify areas for improvement.
- Fine-tune the model further by adjusting parameters, collecting more data, or modifying the architecture.
- Repeat steps 4 to 7 until satisfactory results are achieved.
  
## What I Learned:
   SYCL (Single-source Heterogeneous Programming for OpenCL) and DPC++ (Data Parallel C++) are powerful libraries that facilitate heterogeneous programming and parallel computing. 
