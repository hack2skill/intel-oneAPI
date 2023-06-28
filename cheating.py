import io
import os
from google.cloud import vision

# Set up the Google Cloud Vision client with credentials
credentials_path = 'Files/client_file_vision.json'
client = vision.ImageAnnotatorClient.from_service_account_file(credentials_path)

# Create the folder to store the converted text files
output_folder = 'snips_txt'
os.makedirs(output_folder, exist_ok=True)

# List all files in the "snips" folder
input_folder = 'snips'
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if os.path.isfile(file_path):
        # Open the image file as binary data
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        # Create an image instance
        image = vision.Image(content=content)

        # Perform OCR on the image
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # Extract the detected text
        if texts:
            detected_text = texts[0].description
        else:
            detected_text = 'No text found.'

        # Create the output text file path
        output_filename = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_folder, output_filename)

        # Save the detected text to a text file with UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(detected_text)

        print(f'Converted {filename} to text and saved as {output_filename}.')
