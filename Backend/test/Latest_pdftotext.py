import os
import requests

def convert_pdf_to_text(pdf_url, endpoint_url, credentials_path, service_account_email):
    headers = {
        "Authorization": "Bearer {}".format(get_access_token(credentials_path, service_account_email)),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    request_data = {
        "document": {
            "source": {
                "gcsSource": {
                    "uri": pdf_url
                }
            }
        },
        "destination": {
            "gcsDestination": {
                "uri": ""
            }
        }
    }

    response = requests.post(endpoint_url, headers=headers, json=request_data)
    
    # Check for HTTP errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        print("Response Content:", response.text)
        raise

    print("Response Content:", response.text)  # Print the response content for analysis

    operation_id = response.json()["name"].split("/")[-1]

    operation_url = "{}/{}".format(endpoint_url, operation_id)

    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()

        operation_response = response.json()

        if "done" in operation_response and operation_response["done"]:
            output_gcs_uri = operation_response["response"]["document"]["outputConfig"]["gcsDestination"]["uri"]
            break

    text = requests.get(output_gcs_uri).text

    return text

def get_access_token(credentials_path, service_account_email):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    # Use the Document AI client library to fetch the access token
    from google.auth import impersonated_credentials
    from google.auth.transport import requests
    import google.auth

    target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    credentials, project_id = google.auth.default()

    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=service_account_email,
        target_scopes=target_scopes,
        lifetime=3600,
    )

    request = requests.Request()

    target_credentials.refresh(request)

    return target_credentials.token

import requests
from google.auth import impersonated_credentials
from google.auth.transport import requests as auth_requests
import google.auth

def get_json_from_endpoint(endpoint_url, credentials_path, service_account_email):
    # Set the environment variable with the credentials path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    # Load the service account credentials
    credentials, _ = google.auth.default()

    # Impersonate the service account to obtain access token
    target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=service_account_email,
        target_scopes=target_scopes,
        lifetime=3600,
    )

    # Refresh the target credentials to get an access token
    target_credentials.refresh(auth_requests.Request())

    # Create the headers with the access token
    headers = {
        "Authorization": "Bearer {}".format(target_credentials.token),
        "Accept": "application/json"
    }

    response = requests.get(endpoint_url, headers=headers)

    # Check for HTTP errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        print("Response Content:", response.text)
        return None

    json_data = response.json()
    return json_data
# Set the PDF URL, endpoint URL, and service account credentials path
pdf_url = "https://www.africau.edu/images/default/sample.pdf"
endpoint_url = "https://us-documentai.googleapis.com/v1/projects/32460676396/locations/us/processors/24a37a9507dda54c:process"
credentials_path = "Files/client_file_vision.json"
service_account_email = "image2text@notes2text.iam.gserviceaccount.com"

#Convert PDF to text
result = convert_pdf_to_text(pdf_url, endpoint_url, credentials_path, service_account_email)

# Print the extracted text
print(result)

