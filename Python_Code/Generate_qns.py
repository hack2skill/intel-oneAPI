import openai

# Set up your OpenAI API credentials
openai.api_key = "##"


# Define your input parameters
with open('Local_Storage/Generated_Files/cluster_questions.txt', 'r') as file:
    sorted_questions = str(file.read()) 
with open('#define path for important topics here', 'r') as file:
    important_topics = str(file.read())  
with open('Local_Storage/pyqs_text', 'r', encoding='latin-1') as file:
    reference_paper = str(file.read())            
    
    
# Construct the prompt for question generation
prompt = f"generate 10 questions that are not in reference paper but similar \nSorted Previous Year Questions:\n{sorted_questions}\n\nNotebook Question List:\n{notebook_questions}\n\nImportant Topics:\n{important_topics}\n\nReference Paper:\n{reference_paper}\n\n"


# Generate questions using OpenAI API
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=1000,  # Adjust the max_tokens value as per your requirement
    temperature=0.4,  # Adjust the temperature value to control the creativity of the generated questions
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    n=5  # Adjust the 'n' value to generate more or fewer questions
)

# Extract the generated questions from the API response
generated_questions = [choice['text'].strip() for choice in response.choices]

# Print the generated questions
for i, question in enumerate(generated_questions):
    print(f"Question {i+1}: {question}")    