#pyqsorter , sorts set of pyqs into modules
from fastapi import APIRouter,  Response
import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.cluster import KMeans
from pathlib import Path




# Create an instance of APIRouter
router = APIRouter()

def extract_questions_from_file(filepath):
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    with open(filepath, encoding=encoding) as f:
        content = f.read()
        pattern = r'((?:[IVX]+|\([a-z]\))\. .*(?:\n\s+\(\w\)\. .*)*)'
        matches = re.findall(pattern, content)
        questions = [re.sub(r'\n\s+\(\w\)\. ', ' ', match.strip()) for match in matches]
    return questions


def extract_questions_from_directory(directory):
    questions = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            questions += extract_questions_from_file(filepath)
    return questions

def cluster_questions_1(questions, num_clusters, syllabus_file):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    
    embed = hub.load(module_url)
    embeddings = embed(questions).numpy()
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(embeddings)
    print("ok")
    y_kmeans = kmeans.predict(embeddings)
 
    return y_kmeans

@router.get("/api1")
def api1_handler():
    # Add your logic here
    #print("Extracting question paper text")
    questions = extract_questions_from_directory('Local_Storage/pyqs_text')
    #num_clusters = int(input("To how many clusters do you want to cluster the questions: "))
    num_clusters=4
    syllabus_file = 'Local_Storage/syllabus.txt'
    print("Extracting syllabus")
    labels = cluster_questions_1(questions, num_clusters, syllabus_file)

    print("Clustering questions")
    for i in range(num_clusters):
        cluster_questions = np.array(questions)[np.where(labels == i)[0]]
        print(f"Module {i+1}:")
        for question in cluster_questions:
            print(f" - {question}")




    # Save cluster questions to file
    with open('Local_Storage/Generated_Files/cluster_questions.txt', 'w') as f:
        for i in range(num_clusters):
            cluster_questions = np.array(questions)[np.where(labels == i)[0]]
            f.write(f"Module {i+1}:\n")
            for question in cluster_questions:
                f.write(f" - {question}\n")
            f.write("\n")

    return {"message": "Previous Year question papers sorted to modules"}

@router.post("/api1")
def api1_post_handler():
    # Add your logic here
    return {"message": "POST request received on API 1"}
