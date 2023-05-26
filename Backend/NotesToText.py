import os
from fastapi import APIRouter
from pdf2image import convert_from_path
from google.cloud import vision

# Create an instance of APIRouter
router = APIRouter()

def pdf_to_images(pdf_path, output_folder):
    
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each image in the specified output folder
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.jpeg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    noImg = i+1     
    return image_paths,noImg

@router.get("/NotesToText")
def NotesToText_handler():
    substring_to_remove = "Scanned by CamScanner"
    for i in range(4):
        print(f"converting module-{i+1}....")
        pdf_path = f'Local_Storage/notes_pdf/module_{i+1}.pdf'
        output_folder = f'images/Notes_images/module_{i+1}'
        
        # Convert the PDF to images and save them in the output folder
        image_paths, noImg = pdf_to_images(pdf_path, output_folder)
        print(noImg)
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Files/client_file_vision.json'
        client = vision.ImageAnnotatorClient()

        # [START vision_python_migration_text_detection]
        image_contents = " "

        for j in range(noImg):
            image_path = f'images/Notes_images/Module_{i+1}/page_{j+1}.jpeg'   
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations[0]
                text = str(texts.description)
                image_contents += text.replace(substring_to_remove, "")


        output_file = f"Local_Storage/notes_txt/module_{i+1}.txt"
    #    Write the text content to the output file
        with open(output_file, "w") as file:
            file.write(image_contents)
            print(f"module-{i+1} completed")
              
        if response.error.message:
            raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



