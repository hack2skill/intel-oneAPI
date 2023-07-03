import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import string
import nltk
from nltk.corpus import stopwords
import sklearnex
from sklearnex import patch_sklearn
patch_sklearn() 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
nltk.download('stopwords')
import shutil
import os

def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = " ".join(word for word in text.split() if word not in stop_words)
    
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    return '\n'.join(paragraphs)

import os
def check_plagiarism(file_name):
    # Load student assignment
    student_assignment_file = "D:/Project/Website-Phoenix13/LearnersEd/assignment/models/assign/temp/" + file_name
    reference_assignment_files = [doc for doc in os.listdir('D:/Project/Website-Phoenix13/LearnersEd/assignment/models/assign/') if doc.endswith('.doc') or doc.endswith('.docx')]
    print(student_assignment_file)
    student_assignment = extract_text_from_docx(student_assignment_file)
    processed_student = preprocess_text(student_assignment)
    
    similarities = []
    
    for ref_file in reference_assignment_files:
        # Load reference assignment
        reference_assignment = extract_text_from_docx('D:/Project/Website-Phoenix13/LearnersEd/assignment/models/assign/'+ref_file)
        processed_ref = preprocess_text(reference_assignment)
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([processed_student, processed_ref])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        similarities.append(similarity)
    
    return similarities

check = []

def has_greater_value(check, desired_value):
                return any(element > desired_value for element in check)

def assignment(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension not in ['.doc', '.docx']:
                return JsonResponse({'error': 'Invalid file format'})

            # Specify the directory where you want to save the file
            file_directory = r"D:\Project\Website-Phoenix13\LearnersEd\assignment\models\assign\temp"

            # Create the directory if it doesn't exist
            if not os.path.exists(file_directory):
                return JsonResponse({'error': 'No Save Directory Found'})

            # Save the file to the directory
            file_path = os.path.join(file_directory, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            check = []
            similarities = check_plagiarism(uploaded_file.name)
            for i, similarity in enumerate(similarities):
                check.append(similarity)

            is_accepted = True
            # Perform your assignment evaluation logic here
            plag = (has_greater_value(check, 0.3))  # Replace with your actual evaluation logic

            if plag == False:
                is_accepted = True
                source_file = 'D:/Project/Website-Phoenix13/LearnersEd/assignment/models/assign/temp/' + uploaded_file.name
                destination_directory = 'D:/Project/Website-Phoenix13/LearnersEd/assignment/models/assign'

                # Move the file to the destination directory
                shutil.move(source_file, destination_directory)
            else:
                 is_accepted = False
            # Check if the file exists before deleting
            if os.path.exists(file_path):
                os.remove(file_path)
                print("File deleted successfully.")
            else:
                print("File does not exist.")

            return JsonResponse({'is_accepted': is_accepted})

    return render(request, 'assignment.html', {})
