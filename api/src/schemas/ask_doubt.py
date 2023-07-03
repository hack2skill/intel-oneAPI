"""
Pydantic Models for API's
"""
from typing import Optional, List, Literal
from pydantic import BaseModel
# pylint: disable = line-too-long


class BasicModel(BaseModel):
  """KeyInsights Skeleton Pydantic Model"""
  question: str
  max_answer_length: Optional[int] = 30
  max_seq_length: Optional[int] = 384
  top_n: Optional[int] = 2
  top_k: Optional[int] = 1
  

class AskDoubtModel(BasicModel):
  """Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "question": "<your question>",
            "max_answer_length": 30,
            "max_seq_length": 384,
            "top_n": 2,
            "top_k": 1
        }
    }