import uvicorn
from fastapi import FastAPI

#from Backend.pyqsorter import router as api1_router
#from Backend.summariser import router_summariser as summariser
#from Backend.Notes_Analyser import router as api4_router
from Backend.speech_text import app as api5_router

# import other API routers as needed

app = FastAPI()



# Mount the API routerss
#app.include_router(api1_router)
#app.include_router(summariser)
#app.include_router(api4_router)
app.include_router(api5_router)


# include other API routers as needed

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

