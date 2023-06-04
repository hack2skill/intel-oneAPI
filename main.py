import uvicorn
from fastapi import FastAPI
#from Backend.pyqsorter import router as api1_router
#from Backend.summariser import router_summariser as summariser
#from Backend.test import router_generate_question as generate_question
#from Backend.Notes_Analyser import router as api4_router
# import other API routers as needed
from Backend.updated_sorter import test as test1

app = FastAPI()


# Mount the API routers
#app.include_router(api1_router)
#app.include_router(summariser)
#app.include_router(generate_question)
#app.include_router(api4_router)
app.include_router(test1)
# include other API routers as needed

if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,host='192.168.29.239',reload=True)

