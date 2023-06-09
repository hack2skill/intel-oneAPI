# intel-oneAPI

#### Team Name - Dream Hack
#### Problem Statement - Object detection for autonomous vehicles
#### Team Leader Email - mansibansal7467@gmail.com

## A Brief of the Prototype:
# UML diagram ![image](https://github.com/mansi12340/object_detection_for_autonomous_vehicles_oneAPI/blob/main/Flowchart.png)
  The project aims towards the detection of two main things that have been the major contributors in the road accidents:
  1) object detection= Our project detects the objects in front of the vehicles in a range of 10 metres to 40 metres.
  2)pothole detection= Our project detects the potholes in front of the vehicles in the range 5 metres to 6 metres with accuracy.
  Other than this, our project can detect the object and vehicles in night and in fog which is the most suitable thing to avoid accidents. 
  
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

Step 2: Install required libraries of Intel-openAPI
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
[<img src="data:image/jpeg;base64,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AR8Wy4o+VaseuYWKZnc86r1unpqiO2H5W12ij5WXHE+3Xd9xauT0UzyeFWkMJT6V6n/1Hiz9dxzDEWrpPLy7bRaY2pTt5+lkWsJVM517IafHeUFqimacN+arjujx7vi69aZmZm3PaZm1pnptM9bYxGTjaqpqmZmc5lB8oIKIIggqIICIqAII1WK3yAghIiKgIioAggIgiSqAibQJlCbQqZRwBDeeqZF1pjevh36pnvkyjgvnK4/unmeNy+lb3pTVp4L5657885Xx+f07+/b+5qU8IPxN79yrnPinj8/p39+3911KeEJOIvfuVc58XzOXL12tPrtJqxwfM3bk9NU85fFufp5/W+oeVW3pTaFfOUCAqICCCoghIiCIoCAiKiCANRit8CIIigICIqIICJIgCKiCAiKgIgCoggIioCIIAgiKgIggqICCCoggIioAggI1GK36CAiKgIioAggIgiSqAiCCiCIIKiCEiIoCIICIIKiAggqIISIgiKgAIioggIA1GK3yCIqAAiKiSICIIKIIggIioCIIKIICIqIICAIIioSIggqICCCoggIioCIAIgjUYrfioggIioCIAIgiKgIggogiCCoggIigIggIggqIIgCoggIioggAIiokiAiCAP/Z" width="50%">](https://www.youtube.com/watch?v=Kj6hxT09CPg "Now in Android: 55")
* video 2
```mp4
https://www.youtube.com/watch?v=s-9vVI95zn8
```