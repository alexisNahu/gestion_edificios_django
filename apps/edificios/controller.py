from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from apps.edificios.models import Edificios
from apps.edificios.schema import EdificioRespuesta, EdificioCrear, EdificioActualizar
from apps.edificios.services import EdificiosService
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['edificios'])

@router.get(AppRoutes.EDIFICIOS, response_model=ApiResponse[list[EdificioRespuesta]], status_code=200)
async def get_edificios(
        id: Optional[int] = Query(default=None, ge=1),
        nombre: Optional[str] = Query(default=None, min_length=4, max_length=50),
        status: Optional[bool] = Query(default=None),
        direccion: Optional[str] = Query(default=None, min_length=2, max_length=100),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
    try:
        response: ApiResponse[Edificios] = await edificios_service.get(
            id=id,
            nombre=nombre,
            status=status,
            direccion=direccion,
            page=page,
            page_size=page_size
        )

        return ApiResponse(msg="Edificios obtenidos correctamente", data=response['data'], pagination=response['pagination'], status_code=200)

    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error obteniendo edificios", "details": e.detail, "status_code": e.status_code}
        )

@router.post(AppRoutes.EDIFICIOS, response_model=ApiResponse[EdificioRespuesta], status_code=201)
async def create_edificio(
        payload: EdificioCrear,
        edificios_service: EdificiosService = Depends(EdificiosService)
):
    try:

        edificio: Edificios = await edificios_service.create(payload)
        return ApiResponse(msg="Edificio creado", data=edificio, status_code=201)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error creando edificios", "details": e.detail, "status_code": e.status_code}
        )

@router.put(f"{AppRoutes.EDIFICIOS}/{{id}}", response_model=ApiResponse[EdificioRespuesta], status_code=200)
async def update_edificio(
        id: int,
        payload: EdificioActualizar,
        edificios_service: EdificiosService = Depends(EdificiosService)
):
    try:
        edificio: Edificios = await edificios_service.update(id, payload)
        return ApiResponse(msg="Edificio actualizado", data=edificio, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error actualizando edificio", "details": e.detail, "status_code": e.status_code}
        )

@router.delete(f"{AppRoutes.EDIFICIOS}/{{id}}", response_model=ApiResponse[EdificioRespuesta], status_code=200)
async def delete_edificio(
        id: int,
        edificios_service: EdificiosService = Depends(EdificiosService)
):
    try:
        response: Edificios = await edificios_service.delete(id)
        return ApiResponse(msg="Edificio eliminado correctamente", data=response, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error eliminando edificio", "details": e.detail, "status_code": e.status_code}
        )
