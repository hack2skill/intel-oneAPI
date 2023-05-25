from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/api6')
async def get_text_from_user(request: Request):
    request_body = await request.json()
    user_input = request_body.get("input_text", "")
    file_text = user_input[:200]  # Read the first 200 characters from the user input

    return JSONResponse(content={"blendData": file_text})
