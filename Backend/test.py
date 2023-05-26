import openai
import shutil
import os
import chardet
from fastapi import FastAPI,UploadFile,File
from fastapi import APIRouter


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


    prompt = f"generate 10 questions that are not in reference paper but similar \nSorted Previous Year Questions:\n{decoded_sorted_questions}\n\nNotebook Question List:\n{decoded_notebook_questions}\n\nImportant Topics:\n{decoded_important_topics}\n\nReference Paper:\n{decoded_reference_paper}\n\n"


# Generate questions using OpenAI API
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1000,  # Adjust the max_tokens value as per your requirement
        temperature=0.4,  # Adjust the temperature value to control the creativity of the generated questions
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=5  # Adjust the 'n' value to generate more or fewer questions
    )

    # Extract the generated questions from the API response
    generated_questions = [choice['text'].strip() for choice in response.choices]

    # Print the generated questions
    for i, question in enumerate(generated_questions):
        print(f"Question {i+1}: {question}")   



    return {"dat1" :decoded_sorted_questions,"dat2" : decoded_notebook_questions,"dat3" : decoded_important_topics,"dat4" : decoded_reference_paper}
