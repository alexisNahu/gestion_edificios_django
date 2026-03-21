from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class EdificioCrear(BaseModel):
    nombre: str = Field(min_length=5, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    status: bool = Field(default=True)
    direccion: Optional[str] = Field(default=None, max_length=100)

    @field_validator('nombre', 'descripcion', 'direccion')
    @classmethod
    def no_solo_espacios(cls, v):
        if v is not None and v.strip() == '':
            raise ValueError('El campo no puede contener solo espacios')
        return v.strip() if v else v


class EdificioActualizar(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=50)
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
    model_config = ConfigDict(extra='forbid')

    nombre: Optional[str] = Field(default=None, max_length=50)
    status: Optional[bool] = None
    direccion: Optional[str] = Field(default=None, max_length=100)
