import os
import boto3
from fastapi import APIRouter
import openai
import json

app = APIRouter()
s3_access_key = "AKIAZTHHIOR4JJ5HLTUB"
s3_secret_access_key = "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"
s3_bucket_name = "learnmateai"

s3 = boto3.client("s3", aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_access_key)

# Set up OpenAI API credentials
openai.api_key = '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'

@app.get("/question_gen")
async def summarize_s3_files():
    bucket_name= "learnmateai"
    folder_name= "Notes_Topicwise"
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        for file in response['Contents']:
            file_key = file['Key']
            file_name = os.path.basename(file_key)
            print(file_name)
            summary = await summarize_file(bucket_name, file_key,file_name)
            print(summary)
            save_summary(file_name, summary)
        return {'message': 'Created Notes and saved successfully.'}
    except Exception as e:
        return {'error': str(e)}

async def summarize_file(bucket_name: str, file_key: str, file_name:str):
    try:
        file_name=file_name.split(".txt")[0]
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        prompt = f'create 10 mcq question with 4 option on topic: {file_name} , based on text:{file_content} \n \n output should strictly be a json with array of (question,options,correct option)'
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                                {
                        "role": "user",
                        "content": prompt
                    }
        ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        raise e

def save_summary(file_name: str, summary: str):
    try:
        file_name=file_name.split(".txt")[0]
        save_key = f'Questionare/{file_name}.txt'
        s3.put_object(Body=summary, Bucket=s3_bucket_name, Key=save_key)
    except Exception as e:
        raise e


S3_FOLDER="Questionare/"
@app.get("/get_question")
def read_file(filename: str):
    # Generate the S3 file path
    s3_file_path = os.path.join(S3_FOLDER, filename)

    try:
        # Read the file content from S3
        response = s3.get_object(Bucket=s3_bucket_name, Key=s3_file_path)
        file_content = response["Body"].read().decode("utf-8")

        # Parse the file content as JSON
        json_content = json.loads(file_content)

        # Return the JSON content
        return json_content
    except Exception as e:
        return {"error": str(e)}