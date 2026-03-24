from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

TipoIdentificacion = Literal['Cedula', 'Pasaporte', 'Ruc', 'Licencia']

class InquilinoCrear(BaseModel):
    nombre_completo: str = Field(min_length=5, max_length=60)
    status: bool = Field(default=True)
    telefono: str = Field(min_length=7, max_length=60)
    email: EmailStr
    numero_identificacion: str = Field(min_length=5, max_length=60)
    tipo_identificacion: TipoIdentificacion


class InquilinoActualizar(BaseModel):
    nombre_completo: Optional[str] = Field(default=None, min_length=5, max_length=60)
    status: Optional[bool] = None
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=60)
    email: Optional[EmailStr] = None
    numero_identificacion: Optional[str] = Field(default=None, min_length=5, max_length=60)
    tipo_identificacion: Optional[TipoIdentificacion] = None


class InquilinoRespuesta(BaseModel):
    id: int
    nombre_completo: str
    status: bool
    telefono: str
    email: EmailStr
    numero_identificacion: str
    tipo_identificacion: str

    class Config:
        from_attributes = True


class InquilinoFiltros(BaseModel):
    nombre_completo: Optional[str] = Field(default=None, max_length=60)
    status: Optional[bool] = None
    numero_identificacion: Optional[int] = None
    tipo_identificacion: Optional[TipoIdentificacion] = None
    page: Optional[int] = Field(default=1)
    page_size: Optional[int] = Field(default=10)