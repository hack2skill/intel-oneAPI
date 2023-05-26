from fastapi import APIRouter, Response
from pathlib import Path

router = APIRouter()

@router.get("/clusterqns")
async def generate_file():
    # Read the content of the file from local storage
    file_path = "Local_Storage/Generated_Files/cluster_questions.txt"  # Replace with the actual path to your local file
    with open(file_path, "r") as file:
        file_content = file.read()

    # Set the response to download the file
    return Response(content=file_content, media_type="text/plain")