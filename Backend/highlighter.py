import os
from fastapi import APIRouter, UploadFile, File
from google.cloud import documentai_v1beta3 as documentai

app = APIRouter()

# Configure the Document AI client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Files/client_file_vision.json"
client_options = {"api_endpoint": "https://us-documentai.googleapis.com/v1/projects/32460676396/locations/us/processors/24a37a9507dda54c:process"}  # Replace with your desired endpoint
client = documentai.DocumentProcessorServiceClient(client_options=client_options)

# Define the route for document processing
@app.post("/process_document")
async def process_document(file: UploadFile = File(...)):
    # Save the uploaded file locally
    file_path = f"tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Perform document processing
    project_id = "32460676396"  # Replace with your Google Cloud project ID
    processor_id = "24a37a9507dda54c"  # Replace with your Document AI processor ID

    # Construct the request
    name = f"projects/{project_id}/locations/us/processors/{processor_id}"
    document = {"content": file_path, "mime_type": "application/pdf"}  # Adjust mime_type if uploading a different file type
    request = {"name": name, "document": document}

    # Process the document
    response = client.process_document(request=request)
    operation = response.operation

    # Wait for the operation to complete
    operation.result(timeout=180)  # Set the timeout as needed

    # Retrieve the analyzed document JSON
    operation.refresh()
    if operation.done() and operation.response.document:
        document_json = operation.response.document
        # Extract information from the document JSON as needed
        return {"status": "success", "document_json": document_json}
    else:
        return {"status": "failed"}

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}