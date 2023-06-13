# intel-oneAPI

#### Team Name - Scoops Troops
#### Problem Statement - Object Detection in Autonomous Vehicles.
#### Team Leader Email -jerish716@gmail.com

## A Brief of the Prototype:
  This section must include UML Daigrms and prototype description
  
  **Our object detection prototype is an early version or concept implementation of the object detection system. It serves as a demonstration or initial implementation to showcase the feasibility and functionality of an object detection solution. Object Detection plays the most important role in Autonomous vehicles. Our idea is to add a system that detects the objects even in the blind spots of our vehicle using radiation. Detecting vehicles in blindspots: Most of the time accidents occur because of not knowing about the vehicles in our blindspots, this solution used LiDAR point clouds to alert our system about the vehicles in our blindspots.
 Our prototype aims to detect and localize objects within an image or video stream and also takes radiations as input. Objects to detect includes pedestrians, vehicles, or specific objects of interest. Our prototype uses tensorflow model, which is a pre-trained model . We'll train the model with our new dataset to detect object.
 Our prototype uses LiDAR sensor with it laser light radiations to detect objects in the blind spot.**
   
 **DATA ACQUISITION**:
                      All the necessary data is collected from various sensors including LiDAR, camera and RADAR. A dataset is created using all the aggregated data to work with.

**LANE DETECTION**: 
                    In this part of our prototype, Codes and procedures done for Lane Detection is provided. We use Intel libraries like OpenCV, OneDNN etc,.
                    
Importing Libraries                     : Install all the necessary libraies such as  Numpy , Open CV, Matplotlib , Tensorflow , Scikit learn , Scikit image , one DNN that are optimized with Intel.

Selecting a Pre-trained Model           : We are going to use the pre-trained model OpenCV  to detect lanes.
                                         Intel OpenCV, also known as the Intel Open Source Computer Vision Library, is a powerful and widely used open-source library for computer vision and image processing tasks. It is an optimized version of the popular OpenCV library, tailored specifically for Intel hardware platforms. 

Understanding the Model                : Familiarize yourself with the architecture and specifications of the pretrained object detection model you intend to use. Understand the input format expected by the model, the number and types of output classes, and any specific requirements or constraints.

Load the Pre-trained Model             : This  involves downloading the pretrained model's weights and loading them into the corresponding model architecture.

Coding                                 : It is a pretrained model , So write program codes to perform Lane detection

Optimization of the Model using OneDNN : Load the code file into the Intel OneDNN Architecture .By Providing them with the right coordinates that we used in the code, the OneDNN optimizes our model for more accurate ojutputs.

Evaluation                             : After writing the program code, codes are tested using a sample video.
                                         Upload the video to the text editor and Run the code to get the output.

**OBJECT DETECTION**:
                  Object Detection is totally executed using LiDAR along with other Intel toolkits such as Intel IPP (Integrated Performance Primitives).
        Using LiDAR we can detect the object with the help of lasers from LiDAR . You get a 2D graph of the outline of the object that has been detected by LiDAR.
LiDAR by itself performs Data aquisition , Object Detection and Visualization. LiDAR also calculates the distance at which the object is present from our vehicle with the value of the speed that the laser light takes to bounce back.
  
## Tech Stack: 
   List Down all technologies used to Build the prototype **Clearly mentioning Intel® AI Analytics Toolkits, it's libraries and the SYCL/DCP++ Libraries used**

**Programming Languages**: Python.
**Machine Learning Frameworks**:TensorFlow, Numpy ,MAtplotlib, Scikit learn, scikit image is used for building and training machine
learning models.
**Computer Vision Libraries**: Libraries such as OpenCV can be used for image
processing and computer vision tasks.
**OneAPI Toolkit**: Intel OpenCV , Intel oneAPI Deep Neural Network Library (oneDNN), Intel OneAPI Base toolkit , Intel IPP (Integrated Performance Primitives).
**Development Tools**: Intel Devcloud, version control systems such as Git, VS code 2005 .
**Testing Tools**: Unit testing frameworks such as PyTest will be used for testing
the prototype's functionality.
**Visualization Tool**s: Visualization tools such as Matplotlib and Tensorflow is used. 
   
## Step-by-Step Code Execution Instructions:
               1. Install all the necessary libraries such as opencv, numpy, matplotlib, u scikit learn, scikit image using the install command 
               2. Import all the installed libraries using the import command.
               3. Create a function named 'detect_lanes' that has the following attributes :
                        - The `detect_lanes` function takes a frame (image) as input and performs lane detection on it.
                        - It begins by converting the frame to grayscale using `cv2.cvtColor`.
                        - The grayscale image is then blurred using a Gaussian filter (`cv2.GaussianBlur`) to reduce noise.
                        - Edges are detected in the blurred image using the Canny edge detection algorithm (`cv2.Canny`).
                        - A region of interest (ROI) is defined using vertices to focus on the area where the lanes are expected. The vertices are specified as a list of points.
                        - A mask is created by filling the ROI polygon with white pixels (`cv2.fillPoly`).
                        - The masked edges are obtained by applying the mask using a bitwise AND operation (`cv2.bitwise_and`).
                        - The Hough line transformation (`cv2.HoughLinesP`) is used to detect lines in the masked edges. The parameters control the accuracy and sensitivity of the line detection.
                        - Detected lines are drawn on a blank image (`line_image`) using `cv2.line`.
                        - The detected lane lines are overlaid on the original frame using `cv2.addWeighted` to create the `lane_image`.
                        - The `lane_image` is returned as the output of the function.
               4. Perform Video Processing by following steps: 
                        - Upload the video to the text editor.
                        - The code then sets up a video capture object (`cap`) to read frames from a video file.
                        - A loop is started to process each frame of the video.
                        - The loop reads a frame from the video using `cap.read()`.
                        - If the frame is successfully read (`ret` is True), the `detect_lanes` function is called to process the frame and obtain the processed frame with lane markings.
                        - The processed frame is displayed in a window named "Lane Detection" using `cv2.imshow`.
                        - If the 'q' key is pressed, the loop is terminated.
                        - After the loop ends or the 'q' key is pressed, the video capture is released (`cap.release()`) and all windows are closed (`cv2.destroyAllWindows()`).
  
## What I Learned:
   Write about the biggest learning you had while developing the prototype
   
We learned how to make the maximum use of Intel OneAPI toolkits and to use it on various problem statements as they possess Unified Programming Model, High Performance and Optimization, Extensive Software Ecosystem, Heterogeneous Hardware Support, Scalability and Portability, Developer Productivity, Broad Industry Support. We got familiarized with Intel OneAPI libraries. We learned that using Intel OneDNN for optimization gives a better accuracy than any other methods . We also learned how to run our program codes in GPU with the help of oneAPI toolkits. We learned how to work on Intel Devcloud. We also learned many other technologies and libraries that are integrated with Intel. With got familiarity with all the libraries we used. We got to know more about the different types of sensors that could be integrated with our program to perform object and lane detection.
Apart from that , We also learned to work as a team and collaborate with experts and professionals for efficiency.
