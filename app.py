import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
#from Backend.pyqsorter import router as api1_router
#from Backend.summariser import router_summariser as summariser
from Backend.new_sorter import test as sorter
#from Backend.Notes_Analyser import router as api4_router
#from Backend.Narrator import router as api5_router
from Backend.NotesToText import router as notestotext
# import other API routers as needed

origins = ["*"]


app = FastAPI()
handler=Mangum(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the API routerss
#app.include_router(api1_router)
app.include_router(notestotext)
app.include_router(sorter)
#app.include_router(api4_router)
#app.include_router(api6_router)
#app.include_router(notestotext)

# include other API routers as needed

#app.include_router(NotesToText_rounter)
#app.include_router(api1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

