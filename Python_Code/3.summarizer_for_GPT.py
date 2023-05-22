from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

# Read the contents of the text file
with open("Files\generated_files\summarised_notes\module1_summarized.txt", "r", encoding='utf-8') as file:
    text = file.read()

# Split the text into smaller chunks
max_tokens_per_chunk = 1024  # Initial value
max_words_in_summary = 2000000

# Calculate the maximum number of chunks needed
max_num_chunks = (max_words_in_summary // max_tokens_per_chunk) + 1

# Split the text into chunks
chunks = [text[i:i + max_tokens_per_chunk] for i in range(0, len(text), max_tokens_per_chunk)]

# Generate summaries for each chunk
summaries = []
print("Summarized Note have been divided into chunks:"+str(len(chunks)))
for i, chunk in enumerate(chunks):
    # Reduce the chunk size dynamically if it exceeds the maximum sequence length
    while len(chunk) > max_tokens_per_chunk:
        max_tokens_per_chunk -= 50
    
    try:
        summary = summarizer(chunk, max_length=100, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])
        print(summary[0]['summary_text'])
        print("\n \n STATUS:"+str(i+1)+"/"+str(len(chunks)))
        print("\n \n COMPLETED:"+str((i+1)/len(chunks)*100)+"%")
    except Exception as e:
        print(f"An error occurred while summarizing chunk {i}: {str(e)}")

# Combine the summaries into a single summary
combined_summary = " ".join(summaries)

# Print the combined summary
print("GPT promptable data:")
print(combined_summary)
