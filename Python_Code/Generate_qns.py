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