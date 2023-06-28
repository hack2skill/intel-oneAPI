import openai
import boto3
import json
import requests

openai.api_key = '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'

s3_access_key = "AKIAZTHHIOR4JJ5HLTUB"
s3_secret_access_key = "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"
s3_bucket_name = "learnmateai"


prompt = """you need to analyze a given dataset and return a table with questions appearing more than once. The table should strictly contain questions repeating more than once. The table should also contain the frequency of occurance.Also show the important topics as a diffenrent section at the bottom of the table which is of list format.make the final result in json format.The name of field showing the value of count should be frequency.All the repeating questions must be included in the result under all circumstances.It is important that the output maintains this output format under any circumstances.Only give the json file. Dont return anything other than json.
the dataset is as follows:"""

s3 = boto3.client(
    "s3",
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_access_key
)


def read_object_from_s3(bucket_name, object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    object_content = response['Body'].read().decode('utf-8')
    return object_content

# Usage example
bucket_name = s3_bucket_name
object_key = "Sorted_PYQS/Module1.txt"

object_content = read_object_from_s3(bucket_name, object_key)
#print(object_content)

data =object_content


response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt + data
                }
            ]
        )
important_topics = response.choices[0].message.content

print(important_topics)

dat = important_topics

p1 = "convert this to json and dont miss any information provided under any circumstances. The key of the list of questions should be repeating_questions\n"


response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": p1 + dat
                }
            ]
        )
res = response.choices[0].message.content
resd = json.loads(res)
print("\n\nProcessed")
print(resd)

file_path = "data.json"

# Save the data as JSON in the specified file
with open(file_path, "w") as json_file:
    json.dump(resd, json_file)

print(f"JSON file saved successfully at {file_path}")


with open('data.json', 'r') as file:
    data = json.load(file)

print(data)
# # Extract questions and topics
# questions = data['questions']
# topics = data['important_topics']

# # Create the content for the document
# content = '<h1>Questions</h1>'
# for i, question in enumerate(questions):
#     content += f'<h2>{i+1}. {question["question"]}</h2>'
#     content += f'<p>Frequency: {question["frequency"]}</p>'

# content += '<h1>Important Topics</h1>'
# for topic in topics:
#     content += f'<h2>{topic}</h2>'

# # Convert content to HTML
# html_content = f'''
# <!DOCTYPE html>
# <html>
# <head>
# <title>Document</title>
# </head>
# <body>
# {content}
# </body>
# </html>
# '''

# # Make a POST request to PDFShift API
# api_key = 'c3fc79849a954be4bf9c719cdd3fee52'
# pdfshift_url = 'https://api.pdfshift.io/v3/convert/pdf'

# headers = {'Authorization': f'Bearer {api_key}'}
# payload = {'source': html_content}

# response = requests.post(pdfshift_url, json=payload, headers=headers)

# # Save the generated PDF file
# with open('document.pdf', 'wb') as file:
#     file.write(response.content)