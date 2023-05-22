from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    file_path = 'Local_Storage/pyqs_text/Logic Design  2016 Nov (2015 Ad) (1).txt'  

    with open(file_path, 'r') as file:
        contents = file.read()
    
    return {contents}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
