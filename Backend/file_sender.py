import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
import PyPDF2
import base64
import boto3
import json

aws_access_key_id = ''
aws_secret_access_key =  ''
bucket_name = 'learnmateai'

# Create an S3 client
s3_client = boto3.client("s3",
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
getfiles = APIRouter()

@getfiles.post("/get_notes_txt")
async def retrieve_text_notes(email: str,topic: str):
    # Configure your AWS credentials and region
    

    # Retrieve files from the S3 bucket
    
    prefix = f"{email}/notes_txt"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj["Body"].read().decode("utf-8")
            files.append({"name": file_key, "content": file_content})

    return {"files": files}

@getfiles.post("/get_notes_pdf")
async def retrieve_pdf_files(email: str):
    # Configure your AWS credentials and region
    

    # Retrieve files from the S3 bucket
    
    prefix = f"{email}/notes_pdf"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj["Body"].read()

            # Encode the file content in base64
            encoded_content = base64.b64encode(file_content).decode("utf-8")
            files.append({"name": file_key, "content": encoded_content})

    return {"files": files}

@getfiles.post("/cardData")
def get_cardData(email: str):
    prefix = f"{email}/Cardjson"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
   
    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj["Body"].read().decode("utf-8")
            json_data = json.loads(file_content)
            
    return json_data

@getfiles.post("/studyPlan")
def getStudyPlan(email: str):
    prefix = f"{email}/StudyPlan"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
   
    if "Contents" in response:
        file_key = prefix + "/plan.json"
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_obj["Body"].read().decode("utf-8")
        json_data = json.loads(file_content)
    return json_data

