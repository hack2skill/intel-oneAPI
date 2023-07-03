from fastapi import FastAPI,UploadFile,File
from fastapi import APIRouter
from transformers import pipeline
import shutil
import os
import asyncio
import boto3
from botocore.exceptions import NoCredentialsError


s3_access_key = "AKIAZTHHIOR4CN6UXO6N"
s3_secret_access_key = "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"
s3_bucket_name = "learnmateai"

def save_file_to_s3(filename, content):
    try:
        # Connect to Amazon S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_access_key
        )

        # Set the desired S3 key
        s3_key = f"Generated_Files/Summarised_Notes/summarised_{filename}"

        # Save the file content to Amazon S3
        s3.put_object(Body=content.encode('utf-8'), Bucket=s3_bucket_name, Key=s3_key)

        return {"message": "File uploaded successfully"}
    except NoCredentialsError:
        return {"message": "AWS credentials not found"}





progress = None # just for tracking progress

def summary(text,filename):
    # Load the summarization pipeline
    summarizer = pipeline("summarization")
    # Split the text into smaller chunks
    max_tokens_per_chunk = 1024  # Initial value
    max_words_in_summary = 2000000
    # Calculate the maximum number of chunks needed
    max_num_chunks = (max_words_in_summary // max_tokens_per_chunk) + 1
    # Split the text into chunks
    chunks = [text[i:i + max_tokens_per_chunk] for i in range(0, len(text), max_tokens_per_chunk)]
    # for the exceptions
    exceptions = "NULL"
    global progress
    progress = 0 
    # Generate summaries for each chunk
    summaries = []
    len_chunk=len(chunks)
    print("Note have been divided into chunks:"+str(len_chunk))
    for i, chunk in enumerate(chunks):
        # Reduce the chunk size dynamically if it exceeds the maximum sequence length
        while len(chunk) > max_tokens_per_chunk:
            max_tokens_per_chunk -= 50      
        try:
            summary = summarizer(chunk, max_length=200, min_length=100, do_sample=False)
            summaries.append(summary[0]['summary_text']+"\n\n")
            print(summary[0]['summary_text'])
            print("\n \n STATUS:"+str(i+1)+"/"+str(len_chunk))
            progress = (i+1)/len_chunk*100
            print("\n \n COMPLETED:"+str(progress)+"%")
        except Exception as e:
            print(f"An error occurred while summarizing chunk {i}: {str(e)}")
            exceptions = "\n".join(f"An error occurred while summarizing chunk {i}: {str(e)}")
    # Combine the summaries into a single summary
    combined_summary = " ".join(summaries)
    # Print and return the combined summary
    print("Combined Summary:")
    print(combined_summary)
    with open(f'Local_Storage\Generated_Files\Summarised_Notes\summarised_{filename}', 'w', encoding='utf-8') as file:
        file.write(combined_summary)
    response = save_file_to_s3(filename, combined_summary)
    print(response)
    


async def gen_summary():
                                # reading file
    folder_path = 'Local_Storage\\notes_txt'
    # Get the list of files in the folder
    file_list = os.listdir(folder_path)

    # Iterate over each file in the folder
    for file_name in file_list:
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)

        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            loop = asyncio.get_running_loop()                   # making it to run in background
            await loop.run_in_executor(None, summary, text,file_name)


    


router_summariser = APIRouter()


@router_summariser.post("/get-summary")
async def get_summary():
    await gen_summary()
    return {"status" : 1}

@router_summariser.get("/summary-gen-progress") # route to track progress of summarization
def get_summary_progress():
    global progress
    if progress is None :
        return {"status" : "No summarisation process in progress" }
    elif progress == 100 :
        return {"status" : "Completed" , "value" : progress}
    elif progress in range(0,101) :
        return {"status" : progress}
    else :
        return {"invalid data detected"}