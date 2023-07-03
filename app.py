import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
#from Backend.LatestSorter import app as sorter
#from Backend.Student_analyser import app as progressanalyser
#from Backend.Notes_gen import app as notes_gen
#from Backend.Questionare_Creater import app as gen_question
#from Backend.Sections_topics_json import app as card_gen
#from Backend.summariser import router_summariser as summariser

#from Backend.Notes_Analyser import router as api4_router
#from Backend.Narrator import router as api5_router
#from Backend.NotesChunker import app as chunker 
from Backend.Final_NotesToText import router as notestotxt
#from Backend.Final_Processor import app as processor
#from Backend.Final_NotesChunker import app as chunker
#from Backend.Final_LatestSorter import app as sorter
#from Backend.Final_Sections_topics_json import app as cardmaker
#from Backend.Final_Notes_gen import app as notesgen
#from Backend.Final_Questionare_Creater import app as mcq_gen
#from Backend.Final_email_test import router as email_sender
#from Backend.SortedPQYsender import app as pyqsender
#from Backend.Perfect_video import app as videofinder

# import other API routers as needed

#from Backend.chatbot import bot as botroute

origins = ["*"]


app = FastAPI()
handler=Mangum(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"]
)

# Mount the API routerss


app.include_router(notestotxt)
#app.include_router(email_sender)
#app.include_router(processor)
#app.include_router(chunker)
#app.include_router(sorter)
#app.include_router(cardmaker)
#app.include_router(notesgen)
#app.include_router(mcq_gen)
#app.include_router(chunker)
#app.include_router(pyqsender)

#app.include_router(videofinder)
#app.include_router(botroute)
# include other API routers as needed

#app.include_router(NotesToText_rounter)
#app.include_router(api1_router)

if __name__ == "__main__":
    uvicorn.run(app, host=" 192.168.5.15", port=8010)

