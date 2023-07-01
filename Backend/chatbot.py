import openai
import boto3
from fastapi import APIRouter,Form

openai.api_key = ''

s3_access_key = ""
s3_secret_access_key = ""
s3_bucket_name = "learnmateai"
s3 = boto3.client(
    "s3",
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_access_key
)


def read_file_from_s3(bucket_name, object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read().decode('utf-8')
    return file_content


def chat_bot(module,topic,question):
    
    #module_no = 2
    #topic = "Combinational_Logic.txt"
    file = f"Analysed_Notes/{module}/{topic}.txt"

    data = read_file_from_s3(s3_bucket_name,file)

    print(data)

    user_question = question

    prompt = f"based on the provided topics: {data} answer the question follows : \n {user_question} \n strictly do not answer if it is not related to topics given."

    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt + data
                        }
                    ]
                )
    bot_res = response.choices[0].message.content

    return bot_res


bot = APIRouter()

@bot.post("/chat")
def ChatBot(module_number: str = Form(...), topic: str = Form(...), question: str = Form(...)):
    res = chat_bot(module_number,topic,question)
    return {"response" : res}