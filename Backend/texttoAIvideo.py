from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/api6')
async def get_text_from_file():
    with open('input.txt', 'r') as file:
        file_text = file.read(200)
    return file_text

# Configure CORS
origins = [
    "http://localhost:3000",  # Replace with your frontend URL
    # Add more allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
