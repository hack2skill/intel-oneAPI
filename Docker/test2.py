import boto3
import requests
import base64

# Set AWS S3 bucket names and PDF.co API credentials
source_bucket_name = "srmhack"
destination_bucket_name = "pyqs"
api_key = "angeloantu@gmail.com_8aa65cb24898b55f6d0fa53aef47fc068cddf3eed10448384c51f4536654759d41a30a03"

# Initialize the AWS S3 client
s3 = boto3.client('s3', aws_access_key_id='AKIAZTHHIOR4IBPUFWHE', aws_secret_access_key='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')
print("cred ok")


# Define function to upload file to PDF.co as a temporary file
def upload_file_to_pdfco(file_path):
    # Download PDF file from S3 bucket
    response = s3.get_object(Bucket=source_bucket_name, Key=file_path)
    pdf_data = response["Body"].read()

    # Upload file to PDF.co as a temporary file
    api_url = "https://api.pdf.co/v1/file/upload"
    headers = {"x-api-key": api_key}
    files = {"file": (file_path, pdf_data)}
    response = requests.post(api_url, files=files, headers=headers)

    # Check if API call was successful
    if response.status_code == 200:
        # Extract the uploaded file URL from the API response
        uploaded_file_url = response.json()["url"]
        return uploaded_file_url
    else:
        # Print error message if API call failed
        print("PDF.co API call failed. Status Code:", response.status_code)
        return None


# Define function to convert uploaded file to text using PDF.co API
def convert_to_text(uploaded_file_url):
    # Prepare payload for PDF.co API
    payload = {"url": uploaded_file_url, "async": False}

    # Make API call to PDF.co for PDF to text conversion
    api_url = "https://api.pdf.co/v1/pdf/convert/to/text"
    headers = {"x-api-key": api_key}
    response = requests.post(api_url, data=payload, headers=headers)

    # Check if API call was successful
    if response.status_code == 200:
        # Extract the text from the API response
        result = response.json()
        if result["error"]:
            print("PDF.co API returned an error:", result["message"])
            return None
        else:
            text = result["text"]
            return text
    else:
        # Print error message if API call failed
        print("PDF.co API call failed. Status Code:", response.status_code)
        return None

# Get list of objects in the source S3 bucket
response = s3.list_objects_v2(Bucket=source_bucket_name)

# Loop through all PDF files in the source bucket and convert them to text
for file in response["Contents"]:
    file_key = file["Key"]
    if file_key.endswith(".pdf"):
        uploaded_file_url = upload_file_to_pdfco(file_key)
        if uploaded_file_url is not None:
            text = convert_to_text(uploaded_file_url)
            if text is not None:
                # Save the text to a text file in the destination S3 bucket
                output_file_key = "pyqs_text/" + file_key[:-4] + ".txt"
                s3.put_object(Body=text, Bucket=destination_bucket_name, Key=output_file_key)