import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.cluster import KMeans


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


def cluster_questions(questions, num_clusters, syllabus_file):
    
    

    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    
    embed = hub.load(module_url)
    embeddings = embed(questions).numpy()
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(embeddings)
    print("ok")
    y_kmeans = kmeans.predict(embeddings)
 
    return y_kmeans

questions = extract_questions_from_directory('texts')
num_clusters = int(input("To how many clusters do you want to cluster the questions: "))
syllabus_file = 'syllabus_txt/syllabus.txt'
labels = cluster_questions(questions, num_clusters, syllabus_file)
for i in range(num_clusters):
    cluster_questions = np.array(questions)[np.where(labels == i)[0]]
    print(f"Module {i+1}:")
    for question in cluster_questions:
        print(f" - {question}")
    print()



# Save cluster questions to file
with open('cluster_questions.txt', 'w') as f:
    for i in range(num_clusters):
        cluster_questions = np.array(questions)[np.where(labels == i)[0]]
        f.write(f"Module {i+1}:\n")
        for question in cluster_questions:
            f.write(f" - {question}\n")
        f.write("\n")

