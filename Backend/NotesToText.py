import os
from fastapi import APIRouter,UploadFile,File
from pdf2image import convert_from_path
from google.cloud import vision
from typing import List
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
import tempfile


s3_access_key = "AKIAZTHHIOR4CN6UXO6N"
s3_secret_access_key = "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"
s3_bucket_name = "learnmateai"

s3 = boto3.client("s3", aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_access_key)

# Create an instance of APIRouter

router = APIRouter()

                

def pdf_to_images_from_bytes(pdf_content, output_folder, file_name):
    s3_bucket_name = 'learnmateai'
    
    # Save PDF content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(pdf_content)
    
    # Convert PDF pages to images
    images = convert_from_path(temp_filename)
    
    # Remove the temporary file
    os.remove(temp_filename)

    # Save each image to S3
    image_paths = []
    for i, image in enumerate(images):
        image_bytes = BytesIO()
        image.save(image_bytes, 'JPEG')
        image_bytes.seek(0)
        
        image_key = f'{output_folder}/page_{i+1}.jpeg'
        s3.put_object(Body=image_bytes, Bucket=s3_bucket_name, Key=image_key)
        
        image_paths.append(image_key)
    noImg = i+1     
    return image_paths, noImg

@router.get("/notestotext")
def NotesToText_handler():
    substring_to_remove = "Scanned by CamScanner"
    s3_bucket_name = 'learnmateai'

    
    prefix = 'notes_pdf/'
    
    # List files in the S3 bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=prefix)
    
    # Extract the file names from the response
    files = [obj['Key'] for obj in response.get('Contents', [])]
    
    # Process each file
    for file_name in files:
        file_name = os.path.splitext(os.path.basename(file_name))[0]
        
        print(f"converting {file_name}....")
        
        # Download the PDF file from S3
        pdf_object = s3.get_object(Bucket=s3_bucket_name, Key=f'{prefix}{file_name}.pdf')
        pdf_content = pdf_object['Body'].read()
        
        # Create the output folder in S3
        output_folder = f'images/Notes_images/{file_name}'
        s3.put_object(Body='', Bucket=s3_bucket_name, Key=f'{output_folder}/')
        
        # Convert the PDF to images and save them in the output folder in S3
        image_paths, noImg = pdf_to_images_from_bytes(pdf_content, output_folder, file_name)
        print(noImg)
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Files/client_file_vision.json'
        client = vision.ImageAnnotatorClient()
        
        # [START vision_python_migration_text_detection]
        image_contents = " "
        
        for j in range(noImg):
            image_path = f'{output_folder}/page_{j+1}.jpeg'
            
            # Download the image from S3
            image_object = s3.get_object(Bucket=s3_bucket_name, Key=image_path)
            image_content = image_object['Body'].read()
            
            content = vision.Image(content=image_content)
            response = client.text_detection(image=content)
            texts = response.text_annotations[0]
            text = str(texts.description)
            image_contents += text.replace(substring_to_remove, "")
        
        s3_key = f'notes_txt/{file_name}.txt'
        
        # Upload the text content to S3
        s3.put_object(
            Body=image_contents,
            Bucket=s3_bucket_name,
            Key=s3_key
        )
        
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))



@router.post("/notestotext_modwise")
async def upload_files1(files: List[UploadFile] = File(...)):
    filenames = []

    for file in files:
        contents = await file.read()
        file_obj = BytesIO(contents)
        try:
            s3.upload_fileobj(
                file_obj,
                s3_bucket_name,
                "notes_pdf/" + file.filename,
            )
            filenames.append(file.filename)
        except NoCredentialsError:
            return {"error": "AWS credentials not found."}
    
    return {"filenames": filenames}

@router.post("/notestotext_syllabus")
async def upload_files2(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        file_obj = BytesIO(contents)
        try:
            s3.upload_fileobj(
                file_obj,
                s3_bucket_name,
                "syllabus_pdf/" + file.filename,
            )
            filenames.append(file.filename)
        except NoCredentialsError:
            return {"error": "AWS credentials not found."}
    
    return {"filenames": filenames}

@router.post("/notestotext_pyqs")
async def upload_files3(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        file_obj = BytesIO(contents)
        try:
            s3.upload_fileobj(
                file_obj,
                s3_bucket_name,
                "pyqs_pdf/" + file.filename,
            )
            filenames.append(file.filename)
        except NoCredentialsError:
            return {"error": "AWS credentials not found."}
    
    return {"filenames": filenames}

@router.post("/notestotext_anythingelse")
async def upload_files4(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        file_obj = BytesIO(contents)
        try:
            s3.upload_fileobj(
                file_obj,
                s3_bucket_name,
                "anything_else/" + file.filename,
            )
            filenames.append(file.filename)
        except NoCredentialsError:
            return {"error": "AWS credentials not found."}
    
    return {"filenames": filenames}

@router.get("/")
async def hello():
    return {"hello nigga"}