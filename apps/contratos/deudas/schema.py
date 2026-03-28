from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class DeudaBase(BaseModel):
    # Validamos contra los choices del modelo de Django
    motivo: Literal['Departamento', 'Ande'] = Field(..., description="Motivo de la deuda")
    monto: int = Field(..., gt=0, description="Monto debe ser positivo")
    status: int = Field(default=1, ge=0)
    fecha_comienzo: date = Field(..., description="Fecha en la que se generó la deuda")
    fecha_final: Optional[date] = Field(None, description="Fecha de vencimiento o pago total")


class DeudaCrear(DeudaBase):
    contrato_id: int = Field(..., ge=1)


class DeudaActualizar(BaseModel):
    motivo: Optional[Literal['Departamento', 'Ande']] = None
    monto: Optional[int] = Field(None, gt=0)
    status: Optional[int] = None
    fecha_comienzo: Optional[date] = None
    fecha_final: Optional[date] = None


class DeudaRespuesta(DeudaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contrato_id: int


class DeudaFiltros(BaseModel):
    id: Optional[int] = None
    contrato_id: Optional[int] = None
    motivo: Optional[Literal['Departamento', 'Ande']] = None
    status: Optional[int] = None

    monto__gte: Optional[int] = Field(None, alias="monto_min")
    monto__lte: Optional[int] = Field(None, alias="monto_max")

    fecha_comienzo__gte: Optional[date] = Field(None, alias="fecha_desde")
    fecha_comienzo__lte: Optional[date] = Field(None, alias="fecha_hasta")

    # Filtro especial de Django para saber si algo es nulo o no
    fecha_final__isnull: Optional[bool] = Field(None, alias="pendiente")

    model_config = {
        "extra": "forbid",
        "populate_by_name": True
    }