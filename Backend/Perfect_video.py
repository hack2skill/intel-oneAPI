from fastapi import APIRouter
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
import torch
import boto3


aws_access_key_id = ''
aws_secret_access_key =  ''
bucket_name = 'learnmateai'

    # Create an S3 client
s3_client = boto3.client("s3",
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)



app = APIRouter()

# Load the Universal Sentence Encoder model
model = SentenceTransformer('bert-base-nli-mean-tokens')

# YouTube API parameters
API_KEY = ""
MAX_RESULTS = 5  # Maximum number of search results to retrieve

# Search for videos using the YouTube API
def search_videos(query):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&type=video&maxResults={MAX_RESULTS}&q={query}"
    response = requests.get(url)
    data = json.loads(response.text)
    video_ids = [item['id']['videoId'] for item in data['items']]
    video_titles = [item['snippet']['title'] for item in data['items']]
    return video_ids, video_titles

# Retrieve video transcripts using the YouTube Transcript API
def get_video_transcripts(video_ids):
    transcripts = []
    for video_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = ' '.join([line['text'] for line in transcript])
            transcripts.append(text)
        except:
            transcripts.append('')
    return transcripts

@app.get("/best_video")
def get_best_video(email: str,topic: str):


    prefix = f"{email}/Notes_Topicwise"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if "Contents" in response:
            file_key = prefix + f"/{topic}"
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj["Body"].read().decode("utf-8")
    # Encode the input text
    input_text = file_content

    input_embedding = model.encode([input_text], convert_to_tensor=True)

    # Search for videos and retrieve video transcripts
    video_ids, video_titles = search_videos(input_text)
    video_transcripts = get_video_transcripts(video_ids)

    # Encode the video transcripts
    video_embeddings = model.encode(video_transcripts, convert_to_tensor=True)

    # Calculate the similarity between the input text and video transcripts
    similarity_scores = cosine_similarity(input_embedding, video_embeddings)

    # Rank the videos based on similarity scores
    ranked_videos = sorted(zip(video_ids, video_titles, similarity_scores), key=lambda x: x[2], reverse=True)

    # Select the top-ranked video ID as the best match
    best_video_id = ranked_videos[0][0]

    # Construct the YouTube video URL
    best_video_url = f"https://www.youtube.com/embed/{best_video_id}"

    return {"best_video_url": best_video_url}
