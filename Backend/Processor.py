from fastapi import APIRouter,Form
import httpx

app = APIRouter()

@app.get("/processor")
async def fetch_data(link:str,receiver_email: str ):
    results = []
    
    async with httpx.AsyncClient() as client:
        # Make the first API call
        response1 = await client.get(f"{link}/process_files?user={receiver_email}")
        results.append(response1.json())
        print(response1)
        
        response2 = await client.get(f"{link}/sorter?user={receiver_email}")
        results.append(response2.json())
        print(response2)
        
        response3 = await client.get(f"{link}/card-json?user={receiver_email}")
        results.append(response3.json())
        print(response3)
        
        response4 = await client.get(f"{link}/note_gen?user={receiver_email}")
        results.append(response4.json())
        print(response4)
        
        response5 = await client.get(f"{link}/question_gen?user={receiver_email}")
        results.append(response5.json())
        print(response5)
        
        payload = {
            "receiver_email": receiver_email,
            "subject": "LearnMateAI",
            "message": "Your files have been processed successfully"
        }
        
        response6 = await client.post(link+"/email", data=payload)
        results.append(response6.json())
        print(response6)
    
    return results
