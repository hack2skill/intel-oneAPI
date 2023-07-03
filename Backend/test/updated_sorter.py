#pyqsorter , sorts set of pyqs into modules
from fastapi import APIRouter
import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.cluster import KMeans




# Create an instance of APIRouter
test = APIRouter()

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

def cluster_questions_1(questions, num_clusters):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"

    embed = hub.load(module_url)
    embeddings = embed(questions).numpy()
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(embeddings)
    y_kmeans = kmeans.predict(embeddings)

    # Find repeated questions
    repeated_indices = []
    for i in range(len(questions)):
        if questions[i] in questions[:i]:
            repeated_indices.append(i)

    return y_kmeans, repeated_indices


@test.get("/api1")
def api1_handler():
    questions = extract_questions_from_directory('Local_Storage/pyqs_text')
    num_clusters = 4
    
    labels, repeated_indices = cluster_questions_1(questions, num_clusters)

    print("Clustering questions")
    for i in range(num_clusters):
        cluster_questions = np.array(questions)[np.where(labels == i)[0]]
        print(f"Module {i+1}:")
        for question in cluster_questions:
            print(f" - {question}")

    # Print repeated questions separately
    if repeated_indices:
        print("Repeated Questions:")
        for index in repeated_indices:
            print(f" - {questions[index]}")

    with open('Local_Storage/Generated_Files/cluster_questions.txt', 'w') as f:
        for i in range(num_clusters):
            cluster_questions = np.array(questions)[np.where(labels == i)[0]]
            f.write(f"Module {i+1}:\n")
            for question in cluster_questions:
                f.write(f" - {question}\n")
            f.write("\n")

        # Write repeated questions to file
        if repeated_indices:
            f.write("Repeated Questions:\n")
            for index in repeated_indices:
                f.write(f" - {questions[index]}\n")

    return {"message": "Previous Year question papers sorted to modules"}

@test.post("/api1")
def api1_post_handler():
    # Add your logic here
    return {"message": "POST request received on API 1"}
