from typing import Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, Query

from apps.inquilinos.inquilinos.schema import InquilinoRespuesta, InquilinoCrear, InquilinoActualizar
from apps.inquilinos.inquilinos.services import InquilinosService
from apps.inquilinos.models import Inquilinos
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

inquilinos_router = APIRouter(tags=['inquilinos'])

@inquilinos_router.get(AppRoutes.INQUILINOS, response_model=ApiResponse[list[InquilinoRespuesta]], status_code=200)
async def get_inquilinos(
        id: Optional[int] = Query(default=None, ge=1),
        nombre_completo: Optional[str] = Query(default=None, max_length=60),
        status: Optional[bool] = Query(default=None),
        tipo_identificacion: Optional[Literal['Cedula', 'Pasaporte', 'Ruc', 'Licencia']] = Query(default=None),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        inquilinos_service: InquilinosService = Depends(InquilinosService)
):
    try:
        response: ApiResponse[Inquilinos] = await inquilinos_service.get(
            id=id,
            nombre_completo=nombre_completo,
            status=status,
            tipo_identificacion=tipo_identificacion,
            page=page,
            page_size=page_size
        )
        return ApiResponse(msg="Inquilinos obtenidos correctamente", data=response['data'], pagination=response['pagination'], status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error obteniendo inquilinos", "details": e.detail, "status_code": e.status_code}
        )

@inquilinos_router.post(AppRoutes.INQUILINOS, response_model=ApiResponse[InquilinoRespuesta], status_code=201)
async def create_inquilino(
        payload: InquilinoCrear,
        inquilinos_service: InquilinosService = Depends(InquilinosService)
):
    try:
        inquilino: Inquilinos = await inquilinos_service.create(payload)
        return ApiResponse(msg="Inquilino creado", data=inquilino, status_code=201)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error creando inquilino", "details": e.detail, "status_code": e.status_code}
        )

@inquilinos_router.put(f"{AppRoutes.INQUILINOS}/{{id}}", response_model=ApiResponse[InquilinoRespuesta], status_code=200)
async def update_inquilino(
        id: int,
        payload: InquilinoActualizar,
        inquilinos_service: InquilinosService = Depends(InquilinosService)
):
    try:
        inquilino: Inquilinos = await inquilinos_service.update(id, payload)
        return ApiResponse(msg="Inquilino actualizado", data=inquilino, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error actualizando inquilino", "details": e.detail, "status_code": e.status_code}
        )

@inquilinos_router.delete(f"{AppRoutes.INQUILINOS}/{{id}}", response_model=ApiResponse[InquilinoRespuesta], status_code=200)
async def delete_inquilino(
        id: int,
        inquilinos_service: InquilinosService = Depends(InquilinosService)
):
    try:
        response: Inquilinos = await inquilinos_service.delete(id)
        return ApiResponse(msg="Inquilino eliminado correctamente", data=response, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error eliminando inquilino", "details": e.detail, "status_code": e.status_code}
        )