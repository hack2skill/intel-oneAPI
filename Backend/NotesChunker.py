import tensorflow_hub as hub
from sklearn.cluster import KMeans
import numpy as np
from tqdm import tqdm

# Preprocessing functions
def preprocess_text(text):
    sentences = text.split('\n')  # Split text into sentences
    return sentences

def extract_chunks(text):
    # Preprocess the input text
    sentences = preprocess_text(text)
    
    # Show progress bar while loading the model
    with tqdm(total=1, desc="Loading model") as pbar:
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")
        pbar.update(1)
    
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

# Example usage
text = "This is an example text. It contains multiple sentences.\nEach sentence represents a subsection."
result = extract_chunks(text)
print(result)
