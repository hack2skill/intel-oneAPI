from fastapi import FastAPI,UploadFile,File
from transformers import pipeline
import shutil

async def summary(file: UploadFile = File(...)):

   
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

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
            print("\n \n COMPLETED:"+str((i+1)/len_chunk*100)+"%")
        except Exception as e:
            print(f"An error occurred while summarizing chunk {i}: {str(e)}")
            exceptions = "\n".join(f"An error occurred while summarizing chunk {i}: {str(e)}")

    # Combine the summaries into a single summary
    combined_summary = " ".join(summaries)

    # Print the combined summary
    print("Combined Summary:")
    print(combined_summary)

    return{"summary" : combined_summary,"exceptions" : exceptions}

