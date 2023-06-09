# intel-oneAPI

#### Team Name - Brainwave
#### Problem Statement - Open Innovation in Education
#### Team Leader Email - 

## A Brief of the Prototype <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/81390908-eaae-4fb1-bb79-0fa8f96bd15c" height="80" width="80"> <br>

A neurological condition called dyslexia impairs a person's capacity for reading, writing, and spelling. It affects how the brain interprets language, making it challenging for those with dyslexia to understand written content. Between 5% and 20% of Indians suffer with dyslexia, with urban regions having a higher prevalence of the condition. This indicates that millions of Indian school children experience reading and comprehension problems as a result of this disorder. The creation of solutions like our product Dyslexify, a machine learning initiative intended to help people with dyslexia improve their reading and comprehension skills, has been made possible by technological developments using intel’s oneAPI.

## Features we Offer <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/ab7b93c9-160c-49f1-91f3-853a5aaeaf22" height="80" width="80"> <br>
⭐ 3D model with AR interface usIng oneAPI Rendering toolkit <br>
⭐ Image to speech recognition, text to speech recognition, using SYCL <br>
⭐ ML driven suggestion of books ,using daal4py <br>
⭐ AI Powered Document Assistant, using GPU Strength <br>


## Architecture Diagram <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/136f45e1-5d5a-4aa5-b71b-73a644686216" height="80" width="80"> <br>
<img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/Arch2.png" alt="Logo" height="300">
 


## Tech Stack: <img src="https://github.com/JoelJJoseph/intel-oneAPI/assets/72274851/13362666-adb9-4e7f-ae11-d00ad0339e9e" height="80" width="80"> <br>
* Intel's oneAPI
  * oneDAAL
  * DYC++/SYCL
  * OSPray Studio
  * Rendering Toolkit
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
  
## Augmented-Reality Smart Card
<h2>
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/card1.jpg" alt="Logo" height="200">
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/card2.jpg" alt="Logo" height="200">
</h2> 
<details>
  <summary><h2>3D Model with AR Interface</h2></summary>
  <h3>Introduction</h3>
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/3D.jpg" alt="Logo" height="500">
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/3D2.jpg" alt="Logo" height="500">
 <br>
  <p>Bringing 3D models into the learning process and utilizing an augmented reality interface, students can visualize complex concepts, objects, in a more interactive and engaging manner.    This technology enables students to manipulate and explore virtual objects, enhancing their understanding and retention of the subject matter.</p>
 
  <h3>How we did?</h3>
   
✅ The oneAPI Rendering Toolkit is used to create 3D models, which are then hosted on a WebAR platform for easy accessibility.<br><br>
✅ The models are converted into the glTF format and uploaded to the chosen platform. <br><br>
✅ Users can view and interact with the models through web browsers on various devices, without the need for specialized applications or high-end hardware.<br><br>
✅This combination of powerful rendering tools powered by intel oneAPI and WebAR technology provides a seamless experience for individuals to explore and engage with captivating in augmented reality.
   
 <h3>How to run?</h3>
 1. Visit the website or you can scan the QR code.<br><br>
 2. Give the required permissions to view the 3D AR model.<br><br>
 3. Navigate in the 3D space to view the model from different perspectives.<br><br>
</details>
<details>
  <summary><h2>Image to Speech Recognition</h2></summary>
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
 1. Visit the address /ads/asdasd/asdsa in the this repo.<br><br>
 2. Install the packages mentioned in Requirements.txt <code>pip install -r requirements.txt</code><br><br>
 3. Run this command <code>python app.py</code><br><br>
</details>
<details>
  <summary><h2>ML driven suggestion of books</h2></summary>
  <h3>Introduction</h3>
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/Books.png" alt="Logo" height="400">
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/Books2.png" alt="Logo" height="400">
 <br>
  <p>With This feature , you can bid farewell to the overwhelming task of choosing your next read. The system analyzes your reading history, genre preferences, favorite authors, you will be able to choose what to read next by selecting the book which you already selected. It shows  similar kind of suggestions.</p>
 
<h3>How we did?</h3>  
✅The daal4py is used here.The main purpose of using daal4py in the project is to leverage the optimized implementations of algorithms provided by oneDAL.<br><br>
✅The oneAPI Data Analytics Library (oneDAL) and its Python wrapper, daal4py, are used for computing cosine similarity between vectors.<br><br>
 
 <h3>How to run?</h3>
 1. Visit this website or use this directory /asdas/sadsad if running locally.<br><br>
 2. Run this command <code>python app.py</code><br><br><br><br>
</details>
<details>
  <summary><h2>AI powered Document Assistant</h2></summary>
  <h3>Introduction</h3>
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/pdf1.png" alt="Logo" width="1000">
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/pdf2.png" alt="Logo" width="1000">
 <img src="https://raw.githubusercontent.com/raison024/ArchDiagram/main/pdf3.png" alt="Logo" width="1000">
 <br>
  <p>This is feature  advanced AI-powered document assistant that revolutionizes the way you search and extract information from PDFs. It eliminates the need for manual searching and scrolling through lengthy documents by leveraging the power of GPT-3.5 and Intel oneApi. With PDFGPT, you can effortlessly ask questions and receive instant answers, allowing for efficient and hassle-free document exploration.</p>
 
<h3>How we did?</h3>  
✅Imports the SYCL context from the daal4py.onea pi module.<br><br>
✅This module provides SYCL functionality for GPU acceleration.<br><br>
✅This flexibility allows you to take advantage of the specific strengths of GPUs while maintaining portability across different hardware architectures.<br><br>
✅It is a game-changing tool for researchers, students, and professionals, providing a seamless and effective solution for working with PDF documents.<br><br>
 
 <h3>How to run?</h3>
 1. Visit the website or the address /ads/asdasd/asdsa in the this repo.<br><br>
 2. If running locally run this command <code>cd backend</code> after which <code>python app.py</code><br><br>
 3. Go back to the previous directory using <code>cd ../</code> and navigate to frontend directory using the command <code>cd frontend</code><br><br>
 4. Run this command <code>npm start</code>.<br><br>
</details>
  
## What I Learned:
The Dyslexify project aimed to address the challenges faced by individuals with dyslexia in reading, writing, and comprehension. By leveraging Intel's oneAPI technologies, including the Intel Data Analytics Acceleration Library (DAAL), Intel Math Kernel Library (MKL), and Intel Deep Learning (oneDNN), the project aimed to create a machine learning initiative to improve the lives of students in India and worldwide who struggle with dyslexia.
Through the Dyslexify project and the utilization of Intel's oneAPI technologies, we have learned the transformative impact that technology can have on the lives of individuals with dyslexia. By leveraging machine learning and deep learning capabilities, Dyslexify has the potential to revolutionize the way dyslexic students access, comprehend, and engage with written content. This project serves as a testament to the power of innovation and collaboration in making a positive difference in the lives of millions of dyslexic individuals in India and beyond.
