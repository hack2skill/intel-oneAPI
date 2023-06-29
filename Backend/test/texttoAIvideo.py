from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

router = APIRouter()
app = FastAPI()

@router.get('/api6')
async def get_text_from_file():
    with open('Local_Storage/Generated_Files/narration.txt', 'r') as file:
        file_text = file.read(200)
    return JSONResponse(content={"blendData": file_text})

@router.post('/api7')
async def write_text_to_file(text: str):
    with open('input.txt', 'w') as file:
        file.write(text)
    return JSONResponse(content={"message": "Text successfully written to input.txt"})

app.include_router(router)
