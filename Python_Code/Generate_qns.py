import openai

# Set up your OpenAI API credentials
openai.api_key = "##"


# Define your input parameters
with open('/Users/chemmi/Desktop/SRM-HACK/GenerateQns/input/mod2qns.txt', 'r') as file:
    sorted_questions = str(file.read())
with open('/Users/chemmi/Desktop/SRM-HACK/GenerateQns/input/notes_questions_list.txt', 'r') as file:
    notebook_questions = str(file.read())    
with open('/Users/chemmi/Desktop/SRM-HACK/GenerateQns/input/imp_topic_list.txt', 'r') as file:
    important_topics = str(file.read())  
with open('/Users/chemmi/Desktop/SRM-HACK/GenerateQns/input/referrence.txt', 'r', encoding='latin-1') as file:
    reference_paper = str(file.read())            
    

prompt = f"generate 10 questions that are not in reference paper but similar \nSorted Previous Year Questions:\n{sorted_questions}\n\nNotebook Question List:\n{notebook_questions}\n\nImportant Topics:\n{important_topics}\n\nReference Paper:\n{reference_paper}\n\n"

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