from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string
import numpy as np

app = FastAPI()

# Preprocessing functions
def preprocess_text(text):
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    
    # Remove punctuation and convert to lowercase
    translator = str.maketrans("", "", string.punctuation)
    sentences = [sentence.translate(translator).lower() for sentence in sentences]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    sentences = [[lemmatizer.lemmatize(word) for word in sentence.split()] for sentence in sentences]
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    sentences = [[word for word in sentence if word not in stop_words] for sentence in sentences]
    
    # Convert sentences back to text
    preprocessed_text = [" ".join(sentence) for sentence in sentences]
    return preprocessed_text

# API route for extracting topic-wise chunks
@app.post("/extract_chunks")
def extract_chunks(text: str):
    # Preprocess the input text
    preprocessed_text = preprocess_text(text)
    
    # Vectorize the preprocessed text
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_text)
    
    # Determine the optimal number of clusters using the Elbow Method
    distortions = []
    K = range(1, 10)  # Set the range of possible clusters
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(tfidf_matrix)
        distortions.append(kmeans.inertia_)
    
    # Find the "elbow" point in the distortion plot
    elbow_index = np.argmin(np.diff(distortions)) + 1
    num_clusters = K[elbow_index]
    
    # Perform clustering with the determined number of clusters
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
    
    # Find the closest sentence to each cluster centroid
    closest_indices = pairwise_distances_argmin_min(kmeans.cluster_centers_, tfidf_matrix)
    
    # Retrieve topic-wise chunks
    chunks = []
    for cluster_index, closest_index in enumerate(closest_indices[0]):
        chunk = preprocessed_text[closest_index]
        chunks.append({"topic": f"Topic {cluster_index+1}", "chunk": chunk})
    
    return chunks
