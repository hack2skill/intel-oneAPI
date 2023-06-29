from fastapi import APIRouter
import httpx

app = APIRouter()

@app.get("/fetch-data")
async def fetch_data():
    results = []
    
    async with httpx.AsyncClient() as client:
        # Make the first API call
        response1 = await client.get("https://api.example.com/endpoint1")
        results.append(response1.json())
        
        # Make the second API call
        response2 = await client.get("https://api.example.com/endpoint2")
        results.append(response2.json())
        
        # Make the third API call
        response3 = await client.get("https://api.example.com/endpoint3")
        results.append(response3.json())
    
    return results
