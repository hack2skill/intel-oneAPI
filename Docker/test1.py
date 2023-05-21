import os
import pytesseract
from pdf2image import convert_from_bytes
from PyPDF2 import PdfFileReader
import boto3
from io import BytesIO

# Set the AWS S3 bucket and folder names
bucket_name = "srmhack"
input_folder = "pyqs"
output_folder = "pyqs_text"

# Initialize the AWS S3 client
s3 = boto3.client('s3', aws_access_key_id='AKIAZTHHIOR4IBPUFWHE', aws_secret_access_key='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')
print("cred ok")

# Define a function to convert PDF to text using OCR
def pdf_to_text(file_path):
    response = s3.get_object(Bucket=bucket_name, Key=file_path)
    pdf_data = response['Body'].read()

    pdf_reader = PdfFileReader(BytesIO(pdf_data))
    # Extract text from each page of the PDF file
    text = ""
    for i in range(pdf_reader.numPages):
        # Convert each page of the PDF to an image and apply OCR to extract text
        pil_image = convert_from_bytes(pdf_data, first_page=i+1, last_page=i+1)[0]
        text += pytesseract.image_to_string(pil_image)

    return text

# List objects in the input folder of S3 bucket
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=input_folder+'/')
print(response['Contents'])

# Loop through all PDF files in the input folder and convert them to text
for file in response['Contents']:
    file_key = file['Key']
    if file_key.endswith(".pdf"):
        text = pdf_to_text(file_key)
        # Save the text to a text file in the output folder with the same name as the PDF file
        output_file_key = output_folder + '/' + os.path.splitext(os.path.basename(file_key))[0] + ".txt"
        s3.put_object(Body=text, Bucket=bucket_name, Key=output_file_key)
