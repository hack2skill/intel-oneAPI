from fastapi import FastAPI
from fastapi import APIRouter

app = FastAPI()

# Define a router for the user-related endpoints
router_users = APIRouter()

@router_users.get("/")
def read_root():
    return {"Hello": "World"}

@router_users.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}

# Define a router for the item-related endpoints
router_items = APIRouter()

@router_items.get("/items")
def get_items():
    return {"items": ["item1", "item2", "item3"]}

# Mount the routers on the app
app.include_router(router_users)
app.include_router(router_items)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
