import openai

openai.api_key = "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"

def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def extract_important_topics(questions):
    text = questions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"I will give you a notes summary, this summary may be incomplete in between, but you have to understand it and list down all topics(as Topics) and also list all important topics(as Imp_Topics) and  list down question which can be interpreted(as Questions):\n\n{text}\n\n"
            }
        ]
    )

    important_topics = response.choices[0].message.content
    print(important_topics)
    return important_topics


print("Extracting Prompt data ...")
file_path = 'Files/generated_files/gpt_promt_sum/module2.txt'  # Replace with the actual file path
extracted_text = extract_text_from_file(file_path)
topics = extract_important_topics(extracted_text)

# Extract topics from the topics string
topic_start_index = topics.find("Topics:")
topic_end_index = topics.find("Important topics:")
topic_text = topics[topic_start_index:topic_end_index].strip()

# Extract important topics from the topics string
imp_topic_start_index = topics.find("Imp_Topics:")
imp_topic_end_index = topics.find("Questions:")
imp_topic_text = topics[imp_topic_start_index:imp_topic_end_index].strip()

# Extract Quesions from the topics string
questions_start_index = topics.find("Questions:")
questions_text = topics[questions_start_index:].strip()


# Save topics to topics.txt
with open('Files\generated_files\\topic_list.txt', 'w', encoding='utf-8') as file:
    file.write(topic_text)

# Save important topics to imp_topics.txt
with open('Files\generated_files\imp_topic_list.txt', 'w', encoding='utf-8') as file:
    file.write(imp_topic_text)

# Save questions to questions.txt
with open('D:\SRM HACK\SRM-HACK\Files\generated_files\\notes_questions_list.txt', 'w', encoding='utf-8') as file:
    file.write(questions_text)

print("Topics saved to 'topics.txt'.")
print("Important topics saved to 'imp_topics.txt'.")
print("Questions saved to 'questions.txt'.")