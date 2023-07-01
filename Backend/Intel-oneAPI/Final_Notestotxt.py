import os
from fastapi import APIRouter, UploadFile, File, Form
from pdf2image import convert_from_path
from google.cloud import vision
from typing import List
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
import tempfile
from openvino.inference_engine import IECore

# Set up your S3 credentials and bucket name
s3_access_key = "YOUR_S3_ACCESS_KEY"
s3_secret_access_key = "YOUR_S3_SECRET_ACCESS_KEY"
s3_bucket_name = "YOUR_S3_BUCKET_NAME"

s3 = boto3.client(
    "s3",
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_access_key
)

ie = IECore()

# Create an instance of APIRouter
router = APIRouter()

# Define your OpenVINO model paths
model_xml = "PATH_TO_MODEL_XML"
model_bin = "PATH_TO_MODEL_BIN"

# Load the OpenVINO model
net = ie.read_network(model=model_xml, weights=model_bin)
exec_net = ie.load_network(network=net, device_name="CPU")

# Define the input and output layer names of your model
input_layer_name = "YOUR_INPUT_LAYER_NAME"
output_layer_name = "YOUR_OUTPUT_LAYER_NAME"

# Define any other necessary configuration or parameters

# Rest of the code remains the same...
# ...

@router.post("/filestotext2")
async def NotesToText_handler(user: str = Form(...)):
    user = user + "/"
    prefix = 'notes_pdf/'
    prefix2 = 'pyqs_pdf/'
    
    # Delete existing files in the output folders
    delete_folder_objects(user+'images/Notes_images/')
    delete_folder_objects(user+'notes_txt/')
    
    convert(prefix, user)
    convert(prefix2, user)
    
    return {"process completed"}


def convert(prefix, user):
    # List files in the S3 bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=user+prefix)
    
    # Extract the file names from the response
    files = [obj['Key'] for obj in response.get('Contents', [])]
    
    # Process each file
    for file_name in files:
        file_name = os.path.splitext(os.path.basename(file_name))[0]
        
        print(f"Converting {file_name}....")
        
        # Delete existing files in the output folder
        output_folder = f'{user}images/Notes_images/{file_name}'
        delete_folder_objects(output_folder)
        
        # Download the PDF file from S3
        pdf_object = s3.get_object(Bucket=s3_bucket_name, Key=f'{user}{prefix}{file_name}.pdf')
        pdf_content = pdf_object['Body'].read()
        
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
            
            image_contents += image_content
        
        # Perform text detection using Google Cloud Vision API
        response = client.text_detection(image=vision.Image(content=image_contents))
        texts = response.text_annotations
        
        # Extract the detected text
        detected_text = ""
        for text in texts:
            detected_text += text.description
        
        # Save the detected text in a text file
        text_file_path = f'{user}notes_txt/{file_name}.txt'
        upload_text_to_s3(detected_text, text_file_path)
        
        print(f"{file_name} converted.")
    

def pdf_to_images_from_bytes(pdf_bytes, output_folder, file_name):
    images = convert_from_bytes(pdf_bytes)
    image_paths = []
    noImg = 0
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save each image as JPEG in the output folder
    for i, image in enumerate(images):
        image_path = f'{output_folder}/page_{i+1}.jpeg'
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
        noImg += 1
        
    # Upload images to S3
    upload_images_to_s3(image_paths, file_name)
    
    return image_paths, noImg


def upload_images_to_s3(image_paths, file_name):
    for image_path in image_paths:
        with open(image_path, 'rb') as file:
            try:
                s3.upload_fileobj(file, s3_bucket_name, image_path)
            except NoCredentialsError:
                print("S3 credentials not available.")
            except Exception as e:
                print(f"Error uploading image to S3: {str(e)}")
            finally:
                # Remove the local image file
                os.remove(image_path)


def upload_text_to_s3(text, text_file_path):
    try:
        s3.put_object(Body=text, Bucket=s3_bucket_name, Key=text_file_path)
    except NoCredentialsError:
        print("S3 credentials not available.")
    except Exception as e:
        print(f"Error uploading text file to S3: {str(e)}")


def delete_folder_objects(prefix):
    # List objects in the S3 bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=prefix)
    
    # Extract the object keys from the response
    objects = [obj["Key"] for obj in response.get("Contents", [])]
    
    # Delete each object
    for obj_key in objects:
        s3.delete_object(Bucket=s3_bucket_name, Key=obj_key)

@router.get("/")
async def hello():
    return {"Byte 404 rocks"}
