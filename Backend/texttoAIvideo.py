from fastapi import  APIRouter
from starlette.middleware.cors import CORSMiddleware


router = APIRouter()



@router.get('/api6')
async def get_text_from_file():
    with open('input.txt', 'r') as file:
        file_text = file.read(200)
    return file_text




