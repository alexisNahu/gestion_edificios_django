from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, Body

from apps.finanzas.abonos.schema import AbonoRespuesta, AbonoCrear, AbonoActualizar
from apps.finanzas.abonos.services import AbonosService
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['abonos'])

@router.get(AppRoutes.ABONOS, response_model=ApiResponse[list[AbonoRespuesta]], status_code=200)
async def get_abonos(
        id: Optional[int] = Query(default=None, ge=1),
        pago_id: Optional[int] = Query(default=None, ge=1),
        tipo_pago: Optional[str] = Query(default=None),
        ayuda_dep: Optional[bool] = Query(default=None),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        abonos_service: AbonosService = Depends(AbonosService)
):
    """
    Obtiene la lista de abonos usando los filtros definidos.
    """
    response = await abonos_service.get(
        id=id,
        pago_id=pago_id,
        tipo_pago=tipo_pago,
        ayuda_dep=ayuda_dep,
        page=page,
        page_size=page_size
    )

    return ApiResponse(
        msg="Abonos obtenidos correctamente",
        data=response['data'],
        pagination=response['pagination'],
        status_code=200
    )

@router.post(AppRoutes.ABONOS, response_model=ApiResponse[AbonoRespuesta], status_code=201)
async def create_abono(
        payload: AbonoCrear = Body(...),
        abonos_service: AbonosService = Depends(AbonosService)
):
    """
    Registra un nuevo abono y dispara el recalculado en el modelo Pagos (Django).
    """
    abono: AbonoRespuesta = await abonos_service.create(payload)
    return ApiResponse(msg="Abono registrado correctamente", data=abono, status_code=201)

@router.put(f"{AppRoutes.ABONOS}/{{id}}", response_model=ApiResponse[AbonoRespuesta], status_code=200)
async def update_abono(
        id: int = Path(..., ge=1),
        payload: AbonoActualizar = Body(...),
        abonos_service: AbonosService = Depends(AbonosService)
):
    """
    Actualiza un abono existente por su ID.
    """
    abono: AbonoRespuesta = await abonos_service.update(id, payload)
    return ApiResponse(msg="Abono actualizado correctamente", data=abono, status_code=200)

@router.delete(f"{AppRoutes.ABONOS}/{{id}}", response_model=ApiResponse[AbonoRespuesta], status_code=200)
async def delete_abono(
        id: int = Path(..., ge=1),
        abonos_service: AbonosService = Depends(AbonosService)
):
    """
    Elimina un abono. Se recomienda tener un Signal en Django para el post_delete.
    """
    response: AbonoRespuesta = await abonos_service.delete(id)
    return ApiResponse(msg="Abono eliminado correctamente", data=response, status_code=200)