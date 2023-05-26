import openai
import shutil
import os
from fastapi import FastAPI,UploadFile,File
from fastapi import APIRouter

def temp_file(file):
    try:
        with open("dat.txt", "wb") as buffer:      # saving file
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    with open("temp.txt", "r", encoding='utf-8') as file:
        text = file.read()

    print("Deleting the saved file.......")
    os.remove("temp.txt")
    print("deleted....")       
    return text


router_generate_question = APIRouter()



def gen_questions(file: UploadFile = File(...)):
    text = temp_file(file)  
    return text