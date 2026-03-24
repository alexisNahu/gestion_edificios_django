from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from apps.contratos.contratos.schema import (
    ContratoRespuesta,
    ContratoCrear,
    ContratoActualizar
)
from apps.contratos.contratos.services import ContratosService
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

# Usamos contratos_router para seguir tu convención de nombres
contratos_router = APIRouter(tags=['contratos'])

@contratos_router.get(
    AppRoutes.CONTRATOS,
    # Usamos list[ContratoRespuesta] para que FastAPI sepa que devolvemos una colección
    response_model=ApiResponse[list[ContratoRespuesta]],
    status_code=200
)
async def get_contratos(
        id: Optional[int] = Query(default=None, ge=1),
        inquilino_id: Optional[int] = Query(default=None, ge=1),
        departamento_id: Optional[int] = Query(default=None, ge=1),
        status: Optional[bool] = Query(default=None),
        al_dia: Optional[bool] = Query(default=None),
        frecuencia_pago: Optional[str] = Query(default=None),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        contratos_service: ContratosService = Depends(ContratosService)
):
    try:
        # Pasamos los filtros al service genérico
        response = await contratos_service.get(
            id=id,
            inquilino_id=inquilino_id,
            departamento_id=departamento_id,
            status=status,
            al_dia=al_dia,
            frecuencia_pago=frecuencia_pago,
            page=page,
            page_size=page_size
        )

        return ApiResponse(
            msg="Contratos obtenidos correctamente",
            data=response['data'],
            pagination=response['pagination'],
            status_code=200
        )

    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error obteniendo contratos", "details": e.detail, "status_code": e.status_code}
        )

@contratos_router.post(
    AppRoutes.CONTRATOS,
    response_model=ApiResponse[ContratoRespuesta],
    status_code=201
)
async def create_contrato(
        payload: ContratoCrear,
        contratos_service: ContratosService = Depends(ContratosService)
):
    try:
        # El validador de fechas del schema se ejecutará antes de entrar aquí
        contrato = await contratos_service.create(payload)
        return ApiResponse(msg="Contrato creado exitosamente", data=contrato, status_code=201)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error creando contrato", "details": e.detail, "status_code": e.status_code}
        )

@contratos_router.put(
    f"{AppRoutes.CONTRATOS}/{{id}}",
    response_model=ApiResponse[ContratoRespuesta],
    status_code=200
)
async def update_contrato(
        id: int,
        payload: ContratoActualizar,
        contratos_service: ContratosService = Depends(ContratosService)
):
    try:
        contrato = await contratos_service.update(id, payload)
        return ApiResponse(msg="Contrato actualizado correctamente", data=contrato, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error actualizando contrato", "details": e.detail, "status_code": e.status_code}
        )

@contratos_router.delete(
    f"{AppRoutes.CONTRATOS}/{{id}}",
    response_model=ApiResponse[ContratoRespuesta],
    status_code=200
)
async def delete_contrato(
        id: int,
        contratos_service: ContratosService = Depends(ContratosService)
):
    try:
        contrato = await contratos_service.delete(id)
        return ApiResponse(msg="Contrato eliminado correctamente", data=contrato, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error eliminando contrato", "details": e.detail, "status_code": e.status_code}
        )