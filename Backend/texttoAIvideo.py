from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/api6')
async def get_text_from_file():
    with open('input.txt', 'r') as file:
        file_text = file.read(200)
    return JSONResponse(content=file_text)

# Register the router with the main FastAPI app
app.include_router(router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
