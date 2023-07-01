import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
import boto3


aws_access_key_id = 'AKIAZTHHIOR4JJ5HLTUB'
aws_secret_access_key =  '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'
bucket_name = 'learnmateai'

    # Create an S3 client
s3_client = boto3.client("s3",
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
getfiles = APIRouter()

@getfiles.post("/get_notes_txt")
async def retrieve_files(email: str):
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
async def retrieve_files(email: str):
    # Configure your AWS credentials and region
    

    # Retrieve files from the S3 bucket
    
    prefix = f"{email}/notes_pdf"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj["Body"].read().decode("utf-8")
            files.append({"name": file_key, "content": file_content})

    return {"files": files}