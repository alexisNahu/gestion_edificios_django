from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


# --- ESQUEMA BASE ---
class PagoBase(BaseModel):
    # Usamos Decimal para manejar dinero con precisión (como en tu modelo)
    monto_pagado: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    status: bool = Field(default=True)
    descripcion: Optional[str] = Field(None, description="Nota adicional sobre el pago")


# --- ESQUEMA PARA CREAR ---
class PagoCrear(PagoBase):
    contrato_id: int = Field(..., ge=1)
    # Nota: No incluimos saldo_pendiente porque se calcula en el servidor


# --- ESQUEMA PARA ACTUALIZAR ---
class PagoActualizar(BaseModel):
    monto_pagado: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    status: Optional[bool] = None
    descripcion: Optional[str] = None


# --- ESQUEMA PARA RESPUESTA ---
class PagoRespuesta(PagoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contrato_id: int
    saldo_pendiente: Decimal = Field(..., description="Calculado automáticamente")


# --- ESQUEMA PARA FILTROS ---
class PagoFiltros(BaseModel):
    id: Optional[int] = None
    contrato_id: Optional[int] = None
    status: Optional[bool] = None

    # Filtros de rango para el monto
    monto_pagado__gte: Optional[Decimal] = Field(None, alias="monto_min")
    monto_pagado__lte: Optional[Decimal] = Field(None, alias="monto_max")

    # Búsqueda en la descripción
    descripcion__icontains: Optional[str] = Field(None, alias="nota")

    model_config = {
        "extra": "forbid",
        "populate_by_name": True
    }