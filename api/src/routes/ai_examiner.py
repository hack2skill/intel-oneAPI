""" AI Examiner endpoints """
import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.error import NotFoundErrorResponseModel, InternalServerErrorResponseModel
from schemas.ai_examiner import (
    AIExaminerAskQuestionModel,
    AIExaminerEvalAnswerModel,
    AIExaminerHintMotivateModel
)

from config import AI_EXAMINER_CONFIG
from core.interactive_examiner import InteractiveAIExaminer
from core.llm.base import get_llm

from utils.logging_handler import Logger

router = APIRouter(
    tags=["AI Examiner"],
    responses={500: {
        "model": InternalServerErrorResponseModel
    }})

##################################################################
LLM_METHOD = AI_EXAMINER_CONFIG["llm_method"]
LLM_CONFIG = AI_EXAMINER_CONFIG[LLM_METHOD]
llm = get_llm(llm_method=LLM_METHOD, **LLM_CONFIG)
interactive_ai_examiner = InteractiveAIExaminer.load(
    llm=llm,
    verbose=True
)

@router.post("/ai-examiner/ask-question",
            responses={404: {
                "model": NotFoundErrorResponseModel
            }})
async def create_examiner_ask_question(
    input_payload: AIExaminerAskQuestionModel):
    """Analyze job
    Args:
        input_payload (AIExaminerAskQuestionModel)
    Raises:
        Exception: 500 Internal Server Error if something went wrong
    Returns:
        JSON: Success/Fail Message
    """
    try:
        input_payload_dict = {**input_payload.dict()}

        context = input_payload_dict["context"]
        question_type = input_payload_dict["question_type"]
        topic = input_payload_dict["topic"]

        Logger.info("Input question type: {} around topic {}".format(question_type, topic))
        start_time = time.time()
        is_predicted, output = await interactive_ai_examiner.examiner_ask_question(
           context=context,
           question_type=question_type,
           topic=topic
        )
        end_time = time.time()
        
        Logger.info("🕒 Time taken to get response: {} sec".format(end_time-start_time))
        if is_predicted:
            output.pop("error_message")
            response = {
                "success": True,
                "message": "Successfully predicted the response",
                "data": output
            }
            return JSONResponse(status_code=200, content=response)
        else:
            response = {"success": False, "message": output["error_message"], "data": {}}
            return JSONResponse(status_code=500, content=response)
    except Exception as e:
        response = {"success": False, "message": str(e), "data": {}}
        return JSONResponse(status_code=500, content=response)


@router.post("/ai-examiner/eval-answer",
            responses={404: {
                "model": NotFoundErrorResponseModel
            }})
async def create_examiner_eval_answer(
    input_payload: AIExaminerEvalAnswerModel):
    """Analyze job
    Args:
        input_payload (AIExaminerEvalAnswerModel)
    Raises:
        Exception: 500 Internal Server Error if something went wrong
    Returns:
        JSON: Success/Fail Message
    """
    try:
        input_payload_dict = {**input_payload.dict()}

        ai_question = input_payload_dict["ai_question"]
        student_solution = input_payload_dict["student_solution"]
        topic = input_payload_dict["topic"]

        start_time = time.time()
        is_predicted, output = await interactive_ai_examiner.examiner_eval_answer(
           ai_question=ai_question,
           student_solution=student_solution,
           topic=topic
        )
        end_time = time.time()
        
        Logger.info("🕒 Time taken to get response: {} sec".format(end_time-start_time))
        if is_predicted:
            output.pop("error_message")
            response = {
                "success": True,
                "message": "Successfully predicted the response",
                "data": output
            }
            return JSONResponse(status_code=200, content=response)
        else:
            response = {"success": False, "message": output["error_message"], "data": {}}
            return JSONResponse(status_code=500, content=response)
    except Exception as e:
        response = {"success": False, "message": str(e), "data": {}}
        return JSONResponse(status_code=500, content=response)


@router.post("/ai-examiner/hint-motivate",
            responses={404: {
                "model": NotFoundErrorResponseModel
            }})
async def create_examiner_hint_motivate(
    input_payload: AIExaminerHintMotivateModel):
    """Analyze job
    Args:
        input_payload (AIExaminerHintMotivateModel)
    Raises:
        Exception: 500 Internal Server Error if something went wrong
    Returns:
        JSON: Success/Fail Message
    """
    try:
        input_payload_dict = {**input_payload.dict()}

        ai_question = input_payload_dict["ai_question"]
        student_solution = input_payload_dict["student_solution"] # current incorrect solution
        topic = input_payload_dict["topic"]

        start_time = time.time()
        is_predicted, output = await interactive_ai_examiner.examiner_hint_motivate(
           ai_question=ai_question,
           student_solution=student_solution,
           topic=topic
        )
        end_time = time.time()
        
        Logger.info("🕒 Time taken to get response: {} sec".format(end_time-start_time))
        if is_predicted:
            output.pop("error_message")
            response = {
                "success": True,
                "message": "Successfully predicted the response",
                "data": output
            }
            return JSONResponse(status_code=200, content=response)
        else:
            response = {"success": False, "message": output["error_message"], "data": {}}
            return JSONResponse(status_code=500, content=response)
    except Exception as e:
        response = {"success": False, "message": str(e), "data": {}}
        return JSONResponse(status_code=500, content=response)