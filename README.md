# Tutor AI - Personalized and Adaptive Learning Platform

## Overview
Tutor AI is an advanced AI-powered tutoring system designed to revolutionize traditional learning methods. This GitHub repository introduces Tutor AI, a personalized and adaptive learning platform that aims to enhance the efficiency and effectiveness of learning in any subject area.

## Features
Tutor AI offers the following key features:

1. Personalized Learning: Tutor AI adapts to each student's learning pace and style, delivering educational content tailored to their individual needs.
2. Focus on Key Topics: The system identifies and emphasizes important topics within a subject area, enabling students to prioritize their learning effectively.
3. Instant Feedback: Through regular assessments and testing, Tutor AI provides immediate feedback, allowing students to track their progress and identify areas for improvement.

## How It Works
Tutor AI employs the following approach to provide a personalized and adaptive learning experience:

1. Subject Area Learning: Tutor AI analyzes the provided teacher's notes and comprehends the essential concepts and materials in the subject area.
2. Identification of Key Topics: Based on the analysis of previous year's question papers, Tutor AI identifies the critical topics frequently covered in exams.
3. Adaptive Learning: Tutor AI guides students step by step, focusing on the most important topics and adjusting to their individual learning curve.
4. Engaging Interaction: The system interacts with students as an AI tutor, utilizing its knowledge from teacher's notes and previous question papers to create an engaging and interactive learning experience.
5. Generation of Important Topics and Question Papers: Tutor AI generates important topics and possible question papers to further enhance the learning process and help students prepare for exams.

## Benefits
By leveraging the capabilities of Tutor AI, students can experience the following benefits:

1. Enhanced Concept Comprehension: Tutor AI's personalized and adaptive learning approach improves students' understanding of complex concepts.
2. Achievement of Higher Academic Performance: Through targeted learning and instant feedback, students can achieve better grades and excel academically.

Discover the future of education with Tutor AI and unlock your full learning potential.

## How to Run the Application
To run the Tutor AI application, follow these steps:


1. Set up a virtual environment (recommended) and activate it.
```bash
   virtualenv <your_name>_venv 
   .\<your_name>_venv\Scripts\activate
```
5. Install the required dependencies by running the following command:
    pip install -r <person>_requirements.txt  #example angelo_requirements.txt
6. Once the dependencies are installed, you can start the application by running the following command:
    uvicorn main:app --reload
7. The application will start running locally on your machine.
8. Access the application by opening a web browser and navigating to 
    `http://localhost:8000`.

## API Calls ready

Pyqsorter (takes pyqs text files and syllabus text files from Local Storage and saves output to Generated_files as cluster_question.txt) : `http://localhost:8000/api1`

Notes_Analyser (takes txt from gpt_propt_sum and saves output to Notes_Analyser_Ouput) : `http://localhost:8000/api4`



