import uvicorn
from fastapi import FastAPI

if __name__ == "__main__":
    app1 = FastAPI()
    # Create instances of FastAPI for each API

    # Import and mount the API routers
    from Backend.pyqsorter import router as router1
    app1.include_router(router1)


    # Run the FastAPI applications
    uvicorn.run(app1, host="0.0.0.0", port=8001)

