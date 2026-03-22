# core/schemas.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Pagination(BaseModel):
    paginas_totales: int
    pagina_actual: int
    pagina_siguiente: Optional[int] = None
    pagina_previa: Optional[int] = None

class ApiResponse(BaseModel, Generic[T]):
    msg: str
    status_code: int
    success: bool = True
    data: Optional[T] = None
    pagination: Optional[Pagination] = None