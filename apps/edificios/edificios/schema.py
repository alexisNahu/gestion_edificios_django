from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from typing import Optional

from core.exceptions import BadRequestError


class EdificioCrear(BaseModel):
    nombre: str = Field(min_length=5, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    status: bool = Field(default=True)
    direccion: Optional[str] = Field(default=None, max_length=100)


class EdificioActualizar(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=4, max_length=20)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    status: Optional[bool] = None
    direccion: Optional[str] = Field(default=None, max_length=100)



class EdificioRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    status: bool
    direccion: Optional[str] = None

    class Config:
        from_attributes = True


class EdificioFiltros(BaseModel):
    nombre: Optional[str] = Field(default=None, max_length=50)
    status: Optional[bool] = None
    direccion: Optional[str] = Field(default=None, max_length=100)
    page: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)


