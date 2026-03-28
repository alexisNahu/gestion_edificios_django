from typing import Optional, Literal
from decimal import Decimal
from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class AbonoBase(BaseModel):
    monto: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    tipo_pago: Literal['efectivo', 'transferencia', 'tarjeta']
    descripcion: Optional[str] = None
    ayuda_dep: bool = Field(default=False)

class AbonoCrear(AbonoBase):
    pago_id: int = Field(..., ge=1)

class AbonoActualizar(BaseModel):
    monto: Optional[Decimal] = Field(None, gt=0)
    tipo_pago: Optional[Literal['efectivo', 'transferencia', 'tarjeta']] = None
    descripcion: Optional[str] = None
    ayuda_dep: Optional[bool] = None

class AbonoRespuesta(AbonoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pago_id: int
    fecha: date