# intel-oneAPI

#### Team Name - Brainwave
#### Problem Statement - Open Innovation in Education
#### Team Leader Email - joeljoseph1810@gmail.com
#### Website link - https://joeljjoseph.github.io/Brainwave_Dyslexify/index.html


## Tech Stack: <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/13362666-adb9-4e7f-ae11-d00ad0339e9e" height="80" width="80"> <br>
* Intel's oneAPI
  * oneDAAL
  * DYC++/SYCL
  * Rendering Toolkit
  	* OSPray and OSPray Studio
* Intel's Devcloud
* Python
* Flask
* JavaScript
* OpenAI
* GPT 3.5
* Blender
* Unity
* WebAR
* PythonAnywhere
   
## Step-by-Step Code Execution Instructions:<img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/c1f1a73e-3850-4160-8955-2f1311f2a421" height="80" width="80"> <br>

  This Section must contain set of instructions required to clone and run the prototype, so that it can be tested and deeply analysed


## Image to Speech Recognition <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/1668f35c-922e-443b-9a07-38f4f8895025" height="60" width="60"> <br></summary>

  <h3>Introduction</h3>
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/ImagetoSpeech.jpg" alt="Logo" width="1000">
  <p>This feature enables students to capture images of text, such as medical prescription or text on whiteboards, and convert them into speech. It can assist students with visual    impairments or those who prefer auditory learning, making educational content more accessible.</p>
 
<h3>How we did?</h3>  
✅Create SYCL kernels using the DPC++ programming model provided by the Intel oneAPI Toolkit.<br><br>
✅Compile the SYCL DPC++ code using the DPC++ compiler provided by the Intel oneAPI Toolkit.<br><br>
✅Use ctypes to create a Python wrapper for the compiled C++ code.<br><br>
✅Import the Python wrapper into your Flask application.<br><br>
✅Use the wrapper to call the SYCL DPC++ functions for image processing and speech conversion.<br><br>
 
 <h3>How to run it locally?</h3>
 1. Visit the terminal and type <code>cd Image_to_Speech</code>.<br><br>
 2. Install the packages mentioned in Requirements.txt <code>pip install -r requirements.txt</code><br><br>
 3. Run this command <code>python app.py</code><br><br>


