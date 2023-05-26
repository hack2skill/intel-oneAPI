import os
from fastapi import APIRouter,UploadFile,File
from pdf2image import convert_from_path
from google.cloud import vision
from typing import List


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

@router.get("/notestotext")
def NotesToText_handler():
    substring_to_remove = "Scanned by CamScanner"
    
    folder_path = "Local_Storage/notes_pdf"

    # Get all files in the folder
    mod_files = os.listdir(folder_path)

    # Print the file names
    for file_name in mod_files:
        file_name=file_name.split(".")[0]

        print(f"converting {file_name}....")
        pdf_path = f'Local_Storage/notes_pdf/{file_name}.pdf'
        output_folder = f'images/Notes_images/{file_name}'
        
        # Convert the PDF to images and save them in the output folder
        image_paths, noImg = pdf_to_images(pdf_path, output_folder)
        print(noImg)
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Files/client_file_vision.json'
        client = vision.ImageAnnotatorClient()

        # [START vision_python_migration_text_detection]
        image_contents = " "
        
        for j in range(noImg):
            image_path = f'images/Notes_images/{file_name}/page_{j+1}.jpeg'   
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations[0]
                text = str(texts.description)
                image_contents += text.replace(substring_to_remove, "")


        output_file = f"Local_Storage/notes_txt/{file_name}.txt"
    #    Write the text content to the output file
        with open(output_file, "w",encoding="utf-8") as file:
            file.write(image_contents)
            print(f"{file_name} completed")
              
        if response.error.message:
            raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



@router.post("/notestotext_modwise")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        with open("Local_Storage/notes_pdf/"+file.filename, "wb") as f:
            f.write(contents)
        filenames.append(file.filename)
    return {"filenames": filenames}

@router.post("/notestotext_syllabus")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        with open("Local_Storage/syllabus_pdf"+file.filename, "wb") as f:
            f.write(contents)
        filenames.append(file.filename)
    return {"filenames": filenames}

@router.post("/notestotext_pyqs")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        with open("Local_Storage/pyqs_pdf"+file.filename, "wb") as f:
            f.write(contents)
        filenames.append(file.filename)
    return {"filenames": filenames}

@router.post("/notestotext_anythingelse")
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        contents = await file.read()
        with open("Local_Storage/anything_else/"+file.filename, "wb") as f:
            f.write(contents)
        filenames.append(file.filename)
    return {"filenames": filenames}