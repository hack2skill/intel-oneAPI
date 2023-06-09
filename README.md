# intel-oneAPI

<<<<<<< HEAD
#### Team Name - Dream Hack
#### Problem Statement - Object detection for autonomous vehicles
#### Team Leader Email - mansibansal7467@gmail.com

## A Brief of the Prototype:
# UML diagram ![image](https://github.com/mansi12340/object_detection_for_autonomous_vehicles_oneAPI/blob/main/images/Flowchart.png)
  The project aims towards the detection of two main things that have been the major contributors in the road accidents:
  1) object detection= Our project detects the objects in front of the vehicles in a range of 10 metres to 40 metres.
  2)pothole detection= Our project detects the potholes in front of the vehicles in the range 5 metres to 6 metres with accuracy.
  Other than this, our project can detect the object and vehicles in night and in fog which is the most suitable thing to avoid accidents. 
# Components Used ![image](https://github.com/mansi12340/object_detection_for_autonomous_vehicles_oneAPI/blob/main/images/Components.jpg)
## Tech Stack: 
List of technologies used both in hardware and software
* Raspberry pi 4 board
* LIDAR sensor pro
* Raspberry pi
* camera night vision
* Raspion os
* numactl
* intel-oneAPI
   
## Step-by-Step Code Execution Instructions:
Step 1: CLone the repository
```bash
git clone https://github.com/mansi12340/object_detection_for_autonomous_vehicles_oneAPI object_detection && cd object_detection
```

Step 2: Install the required libraries of Intel-openAPI
```bash
# APT Package Manager
sudo apt install intel-aikit
```
For new Users: 
Note: oneAPI.sh script does the installation work automatically
```bash
# Set up the repository. To do this, download the key to the system keyring:
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \ gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
# Add the signed entry to APT sources and configure the APT client to use the Intel repository:
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
# Update the packages list and repository index.
sudo apt update
```
Step 3: Give run.sh execution permissions
```bash
chmod +x bash.sh
```
Step 4: Execute run.sh
```bash
./run.sh
```

## What I Learned:
  1) We learnt to interface the raspberry pi cam with the raspberry pi board.
  2) How to create a model using intel one API toolkit.
  3) How to detect the potholes and other objects using tensorflow embedding in raspberry pi cam.
  4) How to use LIDAR sensor for the detction of objects

Numactl is a standalone command-line utility that is part of the Linux operating system. It provides a set of commands to control memory allocation and process placement on NUMA systems.

However, you can use Numactl in conjunction with Intel oneAPI to optimize memory access and resource allocation for applications developed using the oneAPI programming model. Here's how you can integrate them:

Application Design: When designing your application with the oneAPI programming model, you can consider the NUMA architecture and memory layout. By understanding the NUMA topology of your system, you can strategically allocate and access memory to minimize latency and improve performance.

Command Invocation: You can invoke Numactl commands within your application code or in the execution environment to set memory placement and process/thread affinity. For example, you can use system calls or execute shell commands from your application to invoke Numactl with the desired options.

Resource Management: Intel oneAPI provides libraries and tools to manage resources and optimize performance for specific hardware architectures, such as CPUs, GPUs, and FPGAs. While Numactl focuses on NUMA-specific memory and process management, oneAPI tools can handle other aspects of resource management, such as task scheduling, workload distribution, and hardware-specific optimizations.

## Highlights
* video 1
```mp4
https://www.youtube.com/watch?v=Kj6hxT09CPg
```
[<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOPNC8IVVkBB_5_yGlAtuFSZZt4R_NujjIOg&usqp=CAU" width="50%">](https://www.youtube.com/watch?v=Kj6hxT09CPg "Now in Android: 55")
* video 2
```mp4
https://www.youtube.com/watch?v=s-9vVI95zn8
```
[<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOPNC8IVVkBB_5_yGlAtuFSZZt4R_NujjIOg&usqp=CAU" width="50%">](https://www.youtube.com/watch?v=s-9vVI95zn8 "Now in Android: 55")
=======
#### Team Name -
#### Problem Statement - 
#### Team Leader Email -

## A Brief of the Prototype:
  This section must include UML Daigrms and prototype description
  
## Tech Stack: 
   List Down all technologies used to Build the prototype **Clearly mentioning Intel® AI Analytics Toolkits, it's libraries and the SYCL/DCP++ Libraries used**
   
## Step-by-Step Code Execution Instructions:
  This Section must contain set of instructions required to clone and run the prototype, so that it can be tested and deeply analysed
  
## What I Learned:
   Write about the biggest learning you had while developing the prototype
>>>>>>> origin/main
