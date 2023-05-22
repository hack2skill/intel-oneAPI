import uvicorn
from fastapi import FastAPI

from api1 import app as app1
from api2 import app as app2
# import other APIs as needed

if __name__ == "__main__":
    uvicorn.run(app1, host="0.0.0.0", port=8001)
    uvicorn.run(app2, host="0.0.0.0", port=8002)
    # run other APIs as needed
