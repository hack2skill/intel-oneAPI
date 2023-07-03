""" Ask Doubt endpoints """
import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.error import NotFoundErrorResponseModel, InternalServerErrorResponseModel
from schemas.ask_doubt import AskDoubtModel

from config import ASK_DOUBT_CONFIG
from core.extractive_qa import ExtractiveQuestionAnswering

from utils.logging_handler import Logger

router = APIRouter(
    tags=["Ask Doubt"],
    responses={500: {
        "model": InternalServerErrorResponseModel
    }})

##################################################################

extractive_qa = ExtractiveQuestionAnswering.load(
    **ASK_DOUBT_CONFIG)

@router.post("/ask-doubt",
            responses={404: {
                "model": NotFoundErrorResponseModel
            }})
async def create_ask_doubt(
    input_payload: AskDoubtModel):
    """Analyze job
    Args:
        input_payload (AskDoubtModel)
    Raises:
        Exception: 500 Internal Server Error if something went wrong
    Returns:
        JSON: Success/Fail Message
    """
    try:
        input_payload_dict = {**input_payload.dict()}

        question = input_payload_dict["question"]

        max_answer_length = input_payload_dict["max_answer_length"]
        max_seq_length = input_payload_dict["max_seq_length"]
        top_n = input_payload_dict["top_n"]
        top_k = input_payload_dict["top_k"]

        Logger.info("Input question: {}".format(question))
        start_time = time.time()
        output = await extractive_qa.predict(
            question=question,
            max_answer_length=max_answer_length,
            max_seq_length=max_seq_length,
            top_n=top_n,
            top_k=top_k
        )
        end_time = time.time()
        
        Logger.info("🕒 Time taken to get response: {} sec".format(end_time-start_time))
        
        response = {
            "success": True,
            "message": "Successfully predicted the response",
            "data": output
        }
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        response = {"success": False, "message": str(e), "data": {}}
        return JSONResponse(status_code=500, content=response)
