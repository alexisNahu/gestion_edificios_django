from pydantic import BaseModel, Field
from typing import Optional


class DepartamentoCrear(BaseModel):
    numero_departamento: str = Field(min_length=1, max_length=20)
    piso: int = Field(ge=0, le=3)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    edificio_id: int = Field(ge=1)
    status: bool = Field(default=True)
    ocupado: bool = Field(default=False)


class DepartamentoActualizar(BaseModel):
    edificio_id: Optional[int]
    numero_departamento: Optional[str] = Field(default=None, min_length=1, max_length=20)
    piso: Optional[int] = Field(default=None, ge=0, le=3)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    status: Optional[bool] = None
    ocupado: Optional[bool] = None


class DepartamentoRespuesta(BaseModel):
    id: int
    numero_departamento: str
    piso: int
    descripcion: Optional[str] = None
    edificio_id: int
    status: bool
    ocupado: bool

    class Config:
        from_attributes = True


class DepartamentoFiltros(BaseModel):
    numero_departamento: Optional[str] = Field(default=None, max_length=20)
    piso: Optional[int] = Field(default=None, ge=0, le=3)
    status: Optional[bool] = None
    ocupado: Optional[bool] = None
    edificio_id: Optional[int] = Field(default=None, ge=1)
    page: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)