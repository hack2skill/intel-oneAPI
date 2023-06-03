import openai
import chardet
from fastapi import FastAPI,UploadFile,File
from fastapi import APIRouter

openai.api_key = "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"  # Replace with your API key

def detect_encoding(data):
    result = chardet.detect(data)
    encoding = result["encoding"]
    return encoding

router_generate_question = APIRouter()


@router_generate_question.post("/gen-questions")
async def gen_questions(sorted_q: UploadFile = File(...),notebook_q: UploadFile = File(...),imp_topics: UploadFile = File(...),ref_paper: UploadFile = File(...)):
    #
    sorted_questions = await sorted_q.read()
    notebook_questions = await notebook_q.read()
    important_topics = await imp_topics.read()
    reference_paper = await ref_paper.read()

    # Decode the file content using the detected encoding
    decoded_sorted_questions = sorted_questions.decode(detect_encoding(sorted_questions))
    decoded_notebook_questions = notebook_questions.decode(detect_encoding(notebook_questions))
    decoded_important_topics = important_topics.decode(detect_encoding(important_topics))
    decoded_reference_paper = reference_paper.decode(detect_encoding(reference_paper))


   



    return {"dat1" :decoded_sorted_questions,"dat2" : decoded_notebook_questions,"dat3" : decoded_important_topics,"dat4" : decoded_reference_paper}
