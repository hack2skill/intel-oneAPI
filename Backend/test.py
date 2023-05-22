from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}

@app.get("/items")
def get_items():
    return {"items": ["item1", "item2", "item3"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
