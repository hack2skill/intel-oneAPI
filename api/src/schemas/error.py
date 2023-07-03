"""
Pydantic models for different status codes
"""
from typing import Optional
from pydantic import BaseModel


class NotFoundErrorResponseModel(BaseModel):
    success: bool = False
    message: Optional[str] = None
    data: Optional[dict] = {}

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": False,
                "message": "Resource not found",
                "data": {}
            }
        }


class InternalServerErrorResponseModel(BaseModel):
    success: bool = False
    message: Optional[str] = "Internal Server Error"
    data: Optional[dict] = {}

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": False,
                "message": "Internal server error",
                "data": {}
            }
        }
