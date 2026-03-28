from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, Query, Path, Body

from apps.finanzas.pagos.schema import PagoRespuesta, PagoCrear, PagoActualizar
from apps.finanzas.pagos.service import PagosService
from apps.finanzas.models import Pagos
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['pagos'])

@router.get(AppRoutes.PAGOS, response_model=ApiResponse[list[PagoRespuesta]], status_code=200)
async def get_pagos(
        id: Optional[int] = Query(default=None, ge=1),
        contrato_id: Optional[int] = Query(default=None, ge=1),
        status: Optional[bool] = Query(default=None),
        monto_min: Optional[Decimal] = Query(default=None, ge=0, alias="monto_pagado__gte"),
        monto_max: Optional[Decimal] = Query(default=None, ge=0, alias="monto_pagado__lte"),
        nota: Optional[str] = Query(default=None, max_length=100, alias="descripcion__icontains"),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        pagos_service: PagosService = Depends(PagosService)
):
    """
    Obtiene la lista de pagos con filtros:
    - ?monto_min=100.50&monto_max=500.00
    - ?nota=marzo (Busca en la descripción)
    - ?contrato_id=5
    """
    response = await pagos_service.get(
        id=id,
        contrato_id=contrato_id,
        status=status,
        monto_pagado__gte=monto_min,
        monto_pagado__lte=monto_max,
        descripcion__icontains=nota,
        page=page,
        page_size=page_size
    )

    return ApiResponse(
        msg="Pagos obtenidos correctamente",
        data=response['data'],
        pagination=response['pagination'],
        status_code=200
    )

@router.post(AppRoutes.PAGOS, response_model=ApiResponse[PagoRespuesta], status_code=201)
async def create_pago(
        payload: PagoCrear = Body(...),
        pagos_service: PagosService = Depends(PagosService)
):
    """
    Registra un pago. El service calculará el saldo_pendiente
    y actualizará el estado 'al_dia' del contrato automáticamente.
    """
    pago: PagoRespuesta = await pagos_service.create(payload)
    return ApiResponse(msg="Pago registrado exitosamente", data=pago, status_code=201)

@router.put(f"{AppRoutes.PAGOS}/{{id}}", response_model=ApiResponse[PagoRespuesta], status_code=200)
async def update_pago(
        id: int = Path(..., ge=1),
        payload: PagoActualizar = Body(...),
        pagos_service: PagosService = Depends(PagosService)
):
    """
    Actualiza datos de un pago existente.
    """
    pago: Pagos = await pagos_service.update(id, payload)
    return ApiResponse(msg="Pago actualizado correctamente", data=pago, status_code=200)

@router.delete(f"{AppRoutes.PAGOS}/{{id}}", response_model=ApiResponse[PagoRespuesta], status_code=200)
async def delete_pago(
        id: int = Path(..., ge=1),
        pagos_service: PagosService = Depends(PagosService)
):
    """
    Elimina un registro de pago.
    """
    pago: Pagos = await pagos_service.delete(id)
    return ApiResponse(msg="Pago eliminado correctamente", data=pago, status_code=200)