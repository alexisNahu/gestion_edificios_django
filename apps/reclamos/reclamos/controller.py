from fastapi import APIRouter, Depends, Query, Path, Body
from typing import Optional

from apps.reclamos.reclamos.schema import (
    ReclamoRespuesta,
    ReclamoCrear,
    ReclamoActualizar,
    ReclamoFiltros
)
from apps.reclamos.reclamos.services import ReclamosService
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['reclamos'])


@router.get(AppRoutes.RECLAMOS, response_model=ApiResponse[list[ReclamoRespuesta]])
async def get_reclamos(
        filtros: ReclamoFiltros = Depends(),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        service: ReclamosService = Depends(ReclamosService)
):
    # Extraemos los filtros limpiando Nones y respetando los nombres de Django (__gte, etc)
    params = filtros.model_dump(exclude_none=True, by_alias=False)

    response = await service.get(
        page=page,
        page_size=page_size,
        **params
    )

    return ApiResponse(
        msg="Reclamos obtenidos correctamente",
        data=response['data'],
        pagination=response['pagination'],
        status_code=200
    )


@router.post(AppRoutes.RECLAMOS, response_model=ApiResponse[ReclamoRespuesta], status_code=201)
async def create_reclamo(
        payload: ReclamoCrear = Body(...),
        service: ReclamosService = Depends(ReclamosService)
):
    # El service ya valida que el contrato_id exista
    nuevo_reclamo = await service.create(payload)
    return ApiResponse(msg="Reclamo registrado con éxito", data=nuevo_reclamo, status_code=201)


@router.put(f"{AppRoutes.RECLAMOS}/{{id}}", response_model=ApiResponse[ReclamoRespuesta])
async def update_reclamo(
        id: int = Path(..., ge=1),
        payload: ReclamoActualizar = Body(...),
        service: ReclamosService = Depends(ReclamosService)
):
    # Usa la lógica genérica de actualización (limpieza de None + Error 404)
    reclamo_editado = await service.update(id, payload)
    return ApiResponse(msg="Reclamo actualizado correctamente", data=reclamo_editado, status_code=200)


@router.delete(f"{AppRoutes.RECLAMOS}/{{id}}", response_model=ApiResponse[ReclamoRespuesta])
async def delete_reclamo(
        id: int = Path(..., ge=1),
        service: ReclamosService = Depends(ReclamosService)
):
    reclamo_eliminado = await service.delete(id)
    return ApiResponse(msg="Reclamo eliminado correctamente", data=reclamo_eliminado, status_code=200)