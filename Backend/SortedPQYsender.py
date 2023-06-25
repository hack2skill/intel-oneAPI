import boto3
import io
from fastapi import APIRouter
import os
import requests
from fastapi.responses import FileResponse

app = APIRouter()

# S3 credentials
AWS_ACCESS_KEY_ID = 'AKIAZTHHIOR4JJ5HLTUB'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = 'learnmateai'
S3_FOLDER_NAME = 'Sorted_PYQS/'

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

PDFSHIFT_API_KEY = 'c3fc79849a954be4bf9c719cdd3fee52'

@app.get("/generate_pdf")
def generate_pdf():
    # Retrieve all text files from the S3 folder
    response = s3_client.list_objects_v2(
        Bucket=S3_BUCKET_NAME,
        Prefix=S3_FOLDER_NAME
    )

    file_names = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.txt')]

    # Generate HTML content
    content = ""

    for i,file_name in enumerate(file_names, start=1):
        # Retrieve text content from each text file
        obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        text_content = obj['Body'].read().decode('utf-8')
        
        # Replace newline characters with <br> tags
        text_content = text_content.replace("\n", "<br>")

        # Define the CSS class and color for the container
        css_class = f"box box-{i % 2 + 1}"  # Alternate between box-1 and box-2
        color = "lightblue" if i % 2 == 1 else "lightgreen"

        # Add heading and content to the HTML
        content += f"<div class='{css_class}'>"
        content += f"<h2>Module {i}</h2>"
        content += f"<p>{text_content}</p>"
        content += "</div>"

    # Prepare the HTML payload
    html_payload = f"""
    <html>
    <head>
        <style>
            .box {{
                margin: 10px;
                padding: 10px;
                font-family: Arial, sans-serif;
                font-size: 12px;
            }}
            .box-1 {{
                background-color: lightblue;
            }}
            .box-2 {{
                background-color: lightgreen;
            }}
        </style>
    </head>
    <body>
        {content}
    </body>
    </html>
    """

    # Convert HTML to PDF using PDFShift API
    response = requests.post(
        'https://api.pdfshift.io/v3/convert/pdf',
        auth=('api',PDFSHIFT_API_KEY),
        json={'source': html_payload,"landscape": False, "use_print": False}
    )

    response.raise_for_status()

    # Save PDF response to a temporary file
    temp_pdf_path = "temp_pdf/temp_pdf.pdf"  # Replace with the desired path to save the temporary PDF file
    with open(temp_pdf_path, "wb") as temp_pdf_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_pdf_file.write(chunk)

    # Return the temporary PDF file
    return FileResponse(temp_pdf_path, filename='combined_pdf.pdf', media_type='application/pdf')