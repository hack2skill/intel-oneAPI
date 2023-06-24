from fastapi import APIRouter
import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearnex import patch_sklearn
import boto3
from botocore.exceptions import NoCredentialsError
patch_sklearn()
from sklearn.cluster import KMeans
import tempfile
from io import BytesIO

# Create an instance of APIRouter
test = APIRouter()

# AWS S3 configuration
AWS_ACCESS_KEY_ID = 'AKIAZTHHIOR4CN6UXO6N'
AWS_SECRET_ACCESS_KEY = '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'
AWS_BUCKET_NAME = 'learnmateai'
AWS_BUCKET_FOLDER = 'pyqs_txt'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def extract_questions_from_file(filepath):
    questions = []
    with open(filepath, 'rb') as file:
        content = file.read()
        encoding = chardet.detect(content)['encoding']
        decoded_content = content.decode(encoding, errors='ignore')
        questions = re.findall(r'\b(?:what|where|why|how|when|which|who|whom|whose)\b.*[?!.]', decoded_content, re.IGNORECASE)
    return questions

def extract_questions_from_directory(directory):
    paginator = s3_client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': AWS_BUCKET_NAME, 'Prefix': directory}

    page_iterator = paginator.paginate(**operation_parameters)

    try:
        if not os.path.exists("temp1/pyqs_txt"):
            os.makedirs("temp1/pyqs_txt")  # Create directory if it doesn't exist
        for page in page_iterator:
            if 'Contents' in page:
                for item in page['Contents']:
                    key = item['Key']
                    local_file_path = os.path.join("temp1/pyqs_txt", os.path.basename(key))  # Use basename of key as local file name
                    try:
                        s3_client.download_file(AWS_BUCKET_NAME, key, local_file_path)
                        print(f"Downloaded {key} to {local_file_path}")
                    except Exception as e:
                        print(f"Failed to download {key}: {str(e)}")
    except Exception as e:
        print(f"An error occurred during pagination: {str(e)}")
        return []

    questions = []
    for filename in os.listdir("temp1/pyqs_txt"):
        filepath = os.path.join("temp1/pyqs_txt", filename)
        if os.path.isfile(filepath):
            questions += extract_questions_from_file(filepath)

    return questions

def cluster_questions(questions, num_clusters):
    if len(questions) == 0:
        return None, []

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
    questions = extract_questions_from_directory(AWS_BUCKET_FOLDER)
    num_clusters = 4

    labels, repeated_indices = cluster_questions(questions, num_clusters)

    print("Clustering questions")
    for i in range(num_clusters):
        cluster_indices = np.where(labels == i)[0]
        cluster_questions = np.array(questions)[cluster_indices]
        print(f"Module {i+1}:")
        for question in cluster_questions:
            print(f" - {question}")

    # Print repeated questions separately
    if repeated_indices:
        print("Repeated Questions:")
        for index in repeated_indices:
            print(f" - {questions[index]}")

    try:
        # Write cluster questions to S3
        cluster_questions_content = ""
        for i in range(num_clusters):
            cluster_indices = np.where(labels == i)[0]
            cluster_questions = np.array(questions)[cluster_indices]
            cluster_questions_content += f"Module {i+1}:\n"
            for question in cluster_questions:
                cluster_questions_content += f" - {question}\n"
            cluster_questions_content += "\n"

        # Write repeated questions to S3
        if repeated_indices:
            cluster_questions_content += "Repeated Questions:\n"
            for index in repeated_indices:
                cluster_questions_content += f" - {questions[index]}\n"

        s3_client.put_object(
            Body=cluster_questions_content.encode(),
            Bucket=AWS_BUCKET_NAME,
            Key='Generated_Files/cluster_questions.txt'
        )

        return {"message": "Previous Year question papers sorted into modules"}
    except NoCredentialsError:
        return {"message": "Failed to write to S3. Credentials not available."}


@test.post("/api1")
def api1_post_handler():
    # Add your logic here
    return {"message": "POST request received on API 1"}
