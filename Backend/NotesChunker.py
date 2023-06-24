from fastapi import APIRouter
import tensorflow_hub as hub
import tensorflow_text
from sklearn.cluster import KMeans
import numpy as np



app = APIRouter()

# Load the USE model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

# Preprocessing functions
def preprocess_text(text):
    sentences = text.split('\n')  # Split text into sentences
    return sentences

# API route for extracting topic-wise chunks
@app.post("/extract_chunks")
def extract_chunks(text: str):
    # Preprocess the input text
    sentences = preprocess_text(text)
    
    # Generate sentence embeddings
    sentence_embeddings = embed(sentences)
    
    # Determine the optimal number of clusters using the Elbow Method
    distortions = []
    K = range(1, 10)  # Set the range of possible clusters
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(sentence_embeddings)
        distortions.append(kmeans.inertia_)
    
    # Find the "elbow" point in the distortion plot
    elbow_index = np.argmin(np.diff(distortions)) + 1
    num_clusters = K[elbow_index]
    
    # Perform clustering with the determined number of clusters
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(sentence_embeddings)
    
    # Retrieve topic-wise chunks with subsections
    chunks = []
    for cluster_index in range(num_clusters):
        chunk_sentences = [sentences[i] for i in range(len(sentences)) if kmeans.labels_[i] == cluster_index]
        chunks.append({"topic": f"Topic {cluster_index+1}", "subsections": chunk_sentences})
    
    return chunks