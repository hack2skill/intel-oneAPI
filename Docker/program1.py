import os
import re
import chardet
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.cluster import KMeans
import boto3

# Initialize the AWS S3 client
s3 = boto3.client('s3', aws_access_key_id='AKIAZTHHIOR4IBPUFWHE', aws_secret_access_key='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')
print("cred ok")


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
    y_kmeans = kmeans.predict(embeddings)
    return y_kmeans

def lambda_handler(event, context):
    # Extract and cluster questions
    bucket_name = "srmhack"
    pyqs_text_folder = "pyqs_text"
    syllabus_file = "syllabus_txt/syllabus.txt"
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    questions = []
    for obj in bucket.objects.filter(Prefix=pyqs_text_folder):
        if obj.key.endswith('.txt'):
            temp_file = "/tmp/" + os.path.basename(obj.key)
            bucket.download_file(obj.key, temp_file)
            questions += extract_questions_from_file(temp_file)
    
    num_clusters = int(event['num_clusters'])
    labels = cluster_questions(questions, num_clusters, syllabus_file)
    
    # Prepare cluster_questions.txt content
    cluster_questions_content = ""
    for i in range(num_clusters):
        cluster_questions = np.array(questions)[np.where(labels == i)[0]]
        cluster_questions_content += f"Module {i+1}:\n"
        for question in cluster_questions:
            cluster_questions_content += f" - {question}\n"
        cluster_questions_content += "\n"
    
    # Save cluster_questions.txt to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key="generated_stuff/cluster_questions.txt",
        Body=cluster_questions_content
    )
    
    # Return a response
    response = {
        'statusCode': 200,
        'body': 'Clustered questions saved to S3'
    }
    
    return response
