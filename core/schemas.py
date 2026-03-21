# core/schemas.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    msg: str
    data: Optional[T] = None
    success: bool = True
    status_code: int