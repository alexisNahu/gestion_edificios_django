from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import date
from decimal import Decimal
from core.exceptions import BadRequestError

FrecuenciaPago = Literal['semanal', 'quincenal', 'mensual', 'bimestral', 'trimestral', 'semestral', 'anual']

class ContratoBase(BaseModel):
    frecuencia_pago: FrecuenciaPago
    monto: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    dia_pago: int = Field(ge=1, le=31)
    fecha_inicio: date
    fecha_fin: date
    descripcion: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode='after')
    def validar_fechas(self) -> 'ContratoBase':
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise BadRequestError("La fecha de inicio no puede ser posterior a la fecha de finalización.")
        return self

class ContratoCrear(ContratoBase):
    inquilino_id: int = Field(ge=1)
    departamento_id: int = Field(ge=1)
    status: bool = Field(default=True)
    al_dia: bool = Field(default=True)

class ContratoActualizar(BaseModel):
    frecuencia_pago: Optional[FrecuenciaPago] = None
    monto: Optional[Decimal] = Field(default=None, ge=0)
    status: Optional[bool] = None
    dia_pago: Optional[int] = Field(default=None, ge=1, le=31)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    al_dia: Optional[bool] = None
    descripcion: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode='after')
    def validar_fechas_update(self) -> 'ContratoActualizar':
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise BadRequestError("La fecha de inicio no puede ser posterior a la fecha de finalización.")
        return self

class ContratoRespuesta(BaseModel):
    id: int
    inquilino_id: int
    departamento_id: int
    frecuencia_pago: str
    monto: Decimal
    status: bool
    dia_pago: int
    fecha_inicio: date
    fecha_fin: date
    al_dia: bool
    descripcion: Optional[str]

    class Config:
        from_attributes = True

class ContratoFiltros(BaseModel):
    id: Optional[int] = None
    inquilino_id: Optional[int] = None
    departamento_id: Optional[int] = None
    status: Optional[bool] = None
    al_dia: Optional[bool] = None
    frecuencia_pago: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)