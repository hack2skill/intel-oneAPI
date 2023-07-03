"""
Pydantic Models for API's
"""
from typing import Optional, List, Literal
from pydantic import BaseModel
# pylint: disable = line-too-long


class BasicModel(BaseModel):
  """KeyInsights Skeleton Pydantic Model"""
  topic: str

class AIExaminerAskQuestionModel(BasicModel):
  """Input Pydantic Model"""
  context: str 
  question_type: Literal['Open Ended', 'Single Choice', 'Multiple Choice', 'Yes or No Choice'] = 'Single Choice' 

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "topic": "Deep Learning",
            "context": "Deep learning is part of a broader family of machine learning methods, \
              which is based on artificial neural networks with representation learning. \
                Learning can be supervised, semi-supervised or unsupervised.",
            "question_type": "Single Choice"
        }
    }

class AIExaminerEvalAnswerModel(BasicModel):
  """Input Pydantic Model"""
  ai_question: str 
  student_solution: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "topic": "Deep Learning",
            "ai_question": "<your_ai_question>",
            "student_solution": "<your_student_solution>"
        }
    }

class AIExaminerHintMotivateModel(BasicModel):
  """Input Pydantic Model"""
  ai_question: str 
  student_solution: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "topic": "Deep Learning",
            "ai_question": "<your_ai_question>",
            "student_solution": "<your_student_solution>"
        }
    }