import uvicorn
from fastapi import FastAPI
#from Backend.pyqsorter import router as api1_router
#from Backend.summariser import router as api2_router
#from Backend.Notes_Analyser import router as api4_router
#from Backend.Narrator import router as api5_router
#from Backend.NotesToText import router as NotesToText_rounter
from Backend.cluster_qns import router as cluster_qns_app
# import other API routers as needed

app = FastAPI()


# Mount the API routers
#app.include_router(api1_router)
#app1.include_router(api2_router)
#app.include_router(api4_router)
#app.include_router(api5_router)
# include other API routers as needed

#app.include_router(NotesToText_rounter)
app.include_router(cluster_qns_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

