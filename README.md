# intel-oneAPI

#### Team Name - Mind Crusaders
#### Problem Statement - Medical Image Processing
#### Team Leader Email - kaamal322@gmail.com

## A Brief of the Prototype:
This project demonstrates the quantization of a Medical Image processing using Intel OpenVINO. Quantization is a compression technique that reduces the memory footprint and computation requirements of a neural network model while maintaining its accuracy. The quantized model can be deployed on resource-constrained devices without compromising performance.
  
## Tech Stack: 
- Intel OpenVINO toolkit
- Python 3.7 or above
- OpenVINO Python API
- OpenCV
- NumPy
- PIL
   
## Step-by-Step Code Execution Instructions:
Step 1: Set up the Environment

Ensure you have installed the required dependencies and libraries, including Intel oneAPI toolkits and OpenVINO.
Make sure you have the appropriate Python environment set up with the necessary packages.
Step 2: Prepare the Model

Place your model files (model.xml and model.bin) in the "./model" directory.
Confirm that the model files exist in the specified directory.
Step 3: Run the Code

Copy the provided code into a Python file (e.g., medical_image_processing.py).
Open a terminal or command prompt and navigate to the directory where the Python file is located.
Step 4: Execute the Code

Run the Python script using the following command:
python model.py 
  
## What I Learned:
I have learned the following key points:

Model Export: The code demonstrates how to export a trained model for deployment using Intel's OpenVINO toolkit. It loads the model from the specified directory, consisting of the model files (model.xml and model.bin), and utilizes the IECore class to read the network and its weights.

Inference Engine: The Intel IECore module is used to load the network onto the CPU device for inference. It provides a unified API to work with different deep learning frameworks and optimizes the execution of the network.

Model Update and Export: After loading the network, the code executes the model on the CPU device to perform network inference. It then exports the updated model, saving it as "updated_model.xml" in the same directory.
