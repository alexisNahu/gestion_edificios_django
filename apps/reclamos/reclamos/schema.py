from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# --- ESQUEMA BASE (Atributos comunes) ---
class ReclamoBase(BaseModel):
    descripcion: str = Field(..., min_length=10, max_length=500, description="Detalle del reclamo")
    status: bool = Field(default=True, description="Estado del reclamo (Abierto/Cerrado)")


class ReclamoCrear(ReclamoBase):
    contrato_id: int = Field(..., ge=1, description="ID del contrato asociado")


class ReclamoActualizar(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=10, max_length=500)
    status: Optional[bool] = None


class ReclamoRespuesta(ReclamoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contrato_id: int
    fecha: date

class ReclamoFiltros(BaseModel):
    # Filtros por ID y Relaciones
    id: Optional[int] = Field(None, ge=1)
    contrato_id: Optional[int] = Field(None, ge=1)

    # Filtros de Texto (Usarán __icontains automáticamente en el Repo)
    descripcion: Optional[str] = Field(None, max_length=100)

    # Filtros de Estado
    status: Optional[bool] = None

    # Filtros Avanzados (Usando el sufijo __ para el Repo)
    fecha__gte: Optional[date] = Field(None, alias="fecha_desde", description="Filtrar desde esta fecha")
    fecha__lte: Optional[date] = Field(None, alias="fecha_hasta", description="Filtrar hasta esta fecha")

    model_config = {
        "extra": "forbid",  # Evita que manden filtros que no existen
        "populate_by_name": True  # Permite usar 'desde' en la URL pero mapearlo a 'fecha__gte'
    }

