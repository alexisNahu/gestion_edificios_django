from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, Path, Body

from apps.contratos.deudas.schema import DeudaRespuesta, DeudaCrear, DeudaActualizar
from apps.contratos.deudas.service import DeudaService
from apps.contratos.models import Deuda
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['deudas'])

@router.get(AppRoutes.DEUDAS, response_model=ApiResponse[list[DeudaRespuesta]], status_code=200)
async def get_deudas(
        id: Optional[int] = Query(default=None, ge=1),
        contrato_id: Optional[int] = Query(default=None, ge=1),
        status: Optional[int] = Query(default=None),
        motivo: Optional[str] = Query(default=None),
        monto_min: Optional[int] = Query(default=None, ge=0, alias="monto__gte"),
        monto_max: Optional[int] = Query(default=None, ge=0, alias="monto__lte"),
        desde: Optional[date] = Query(default=None, alias="fecha_comienzo__gte"),
        hasta: Optional[date] = Query(default=None, alias="fecha_comienzo__lte"),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        deuda_service: DeudaService = Depends(DeudaService)
):
    response = await deuda_service.get(
        id=id,
        contrato_id=contrato_id,
        status=status,
        motivo=motivo,
        monto__gte=monto_min,
        monto__lte=monto_max,
        fecha_comienzo__gte=desde,
        fecha_comienzo__lte=hasta,
        page=page,
        page_size=page_size
    )

    return ApiResponse(
        msg="Deudas obtenidas correctamente",
        data=response['data'],
        pagination=response['pagination'],
        status_code=200
    )

@router.post(AppRoutes.DEUDAS, response_model=ApiResponse[DeudaRespuesta], status_code=201)
async def create_deuda(
        payload: DeudaCrear = Body(...),
        deuda_service: DeudaService = Depends(DeudaService)
):
    deuda: DeudaRespuesta = await deuda_service.create(payload)
    return ApiResponse(msg="Deuda creada correctamente", data=deuda, status_code=201)

@router.put(f"{AppRoutes.DEUDAS}/{{id}}", response_model=ApiResponse[DeudaRespuesta], status_code=200)
async def update_deuda(
        id: int = Path(..., ge=1),
        payload: DeudaActualizar = Body(...),
        deuda_service: DeudaService = Depends(DeudaService)
):
    deuda: Deuda = await deuda_service.update(id, payload)
    return ApiResponse(msg="Deuda actualizada correctamente", data=deuda, status_code=200)

@router.delete(f"{AppRoutes.DEUDAS}/{{id}}", response_model=ApiResponse[DeudaRespuesta], status_code=200)
async def delete_deuda(
        id: int = Path(..., ge=1),
        deuda_service: DeudaService = Depends(DeudaService)
):
    deuda: Deuda = await deuda_service.delete(id)
    return ApiResponse(msg="Deuda eliminada correctamente", data=deuda, status_code=200)