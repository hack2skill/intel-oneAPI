from fastapi import APIRouter


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