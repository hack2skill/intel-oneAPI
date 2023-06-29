from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1 import types

def extract_text_from_pdf(project_id, location, processor_id, input_uri):
    client = documentai.DocumentProcessorServiceClient()

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    request = types.ProcessRequest(
        name=name,
        input_config=types.InputConfig(gcs_source=input_uri),
        document_type="application/pdf",
        output_config=types.OutputConfig(gcs_destination={"uri": "gs://<BUCKET_NAME>/<OUTPUT_PREFIX>"}),
    )

    result = client.process_document(request=request)

    output_uri = result.document.output_config.gcs_destination.uri
    print(f"Output stored in {output_uri}")

    return output_uri

# Set your GCP project ID, location, processor ID, and input PDF URI
project_id = "notes2text"
location = "us"  # e.g., "us" or "eu"
processor_id = "24a37a9507dda54c"
input_uri = "Local_Storage/notes_pdf/EE2-695-2019_Scheme-2023 (8).pdf"

extracted_text_uri = extract_text_from_pdf(project_id, location, processor_id, input_uri)


from google.cloud import documentai_v1beta3 as documentai

def extract_pdf_content(file_path):
   project_id = "notes2text"
   location = "us"  # e.g., "us" or "eu"
   processor_id = "24a37a9507dda54c"
   client = documentai.DocumentProcessorServiceClient()
   
   processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
   
   with open(file_path, "rb") as file:
       content = file.read()

    # Configure the input document
   input_config = documentai.types.document_processor_service.BatchProcessRequest.BatchInputConfig(
       gcs_source=None, content=content
    )

    # Configure the output document
   output_config = documentai.types.document_processor_service.BatchProcessRequest.BatchOutputConfig(
       gcs_destination=None  # Set to None for local storage
    )

    # Set up the request
   request = documentai.types.document_processor_service.BatchProcessRequest(
       name=processor_name,
       input_configs=[input_config],
       output_config=output_config,
    )

    # Process the document
   operation = client.batch_process_documents(request=request)
   operation.result()

    # Retrieve the results
   results = operation.response.payload

    # Extract the content from the first page
   first_page = results[0].document.pages[0]
   content = first_page.layout.text_anchor.text

    # Write the content to a local file
   output_file_path = "/Local_Storage/Generated_Files/documentocr.txt"
   with open(output_file_path, "w", encoding="utf-8") as output_file:
       output_file.write(content)

   print(f"Content extracted and stored in {output_file_path}")

# Usage
file_path = "/Local_Storage/notes_pdf/EE2-695-2019_Scheme-2023 (8).pdf"
extract_pdf_content(file_path)
