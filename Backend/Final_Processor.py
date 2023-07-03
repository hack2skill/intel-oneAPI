from fastapi import APIRouter,Form
import httpx

app = APIRouter()

@app.get("/processor")
async def fetch_data(link:str,receiver_email: str ):
    results = []
    
    async with httpx.AsyncClient(timeout=3000.0) as client:
        # Make the first API call
        response1 = await client.get(f"{link}/process_files?user={receiver_email}")
        print(response1)
        response2 = await client.get(f"{link}/sorter?user={receiver_email}")
        print(response2)
        response3 = await client.get(f"{link}/card-json?user={receiver_email}")
        
        response4 = await client.get(f"{link}/note_gen?user={receiver_email}")
        
        response5 = await client.get(f"{link}/question_gen?user={receiver_email}")

        
        
        payload = {
            "receiver_email": receiver_email,
            "subject": "LearnMateAI",
            "message": "Your files have been processed successfully"
        }

        response6 = await client.post(f"{link}/email", data=payload)


