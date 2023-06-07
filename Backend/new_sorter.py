from fastapi import APIRouter
import io
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearnex import patch_sklearn
patch_sklearn()
from sklearn.cluster import KMeans
import boto3

# Create an instance of APIRouter
test = APIRouter()

def extract_questions_from_file(file_content):
    pattern = r'((?:[IVX]+|\([a-z]\))\. .*(?:\n\s+\(\w\)\. .*)*)'
    matches = re.findall(pattern, file_content)
    questions = [re.sub(r'\n\s+\(\w\)\. ', ' ', match.strip()) for match in matches]
    return questions

def extract_questions_from_s3(bucket, key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return extract_questions_from_file(content)

def cluster_questions(questions, num_clusters):
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
    s3_bucket = 'learnmateai'
    s3_key_prefix = 'pyqs_text/'
    num_clusters = 4
    
    s3 = boto3.client('s3')
    questions = []
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_key_prefix)
    for obj in response['Contents']:
        key = obj['Key']
        if key.endswith('.txt'):
            response = s3.get_object(Bucket=s3_bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            questions += extract_questions_from_file(content)

    labels, repeated_indices = cluster_questions(questions, num_clusters)

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

    # Save the results to S3
    output_key = 'Generated_Files/cluster_questions.txt'
    output_content = ""
    for i in range(num_clusters):
        cluster_questions = np.array(questions)[np.where(labels == i)[0]]
        output_content += f"Module {i+1}:\n"
        for question in cluster_questions:
            output_content += f" - {question}\n"
        output_content += "\n"

    if repeated_indices:
        output_content += "Repeated Questions:\n"
        for index in repeated_indices:
            output_content += f" - {questions[index]}\n"

    s3.put_object(Body=output_content.encode('utf-8'), Bucket=s3_bucket, Key=output_key)

    return {"message": "Previous Year question papers sorted to modules"}

@test.post("/api1")
def api1_post_handler():
    # Add your logic here
    return {"message": "POST request received on API 1"}
