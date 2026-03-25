from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body

from apps.edificios.edificios.schema import EdificioRespuesta, EdificioCrear, EdificioActualizar
from apps.edificios.edificios.services import EdificiosService
from apps.edificios.models import Edificios
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['edificios'])

@router.get(AppRoutes.EDIFICIOS, response_model=ApiResponse[list[EdificioRespuesta]], status_code=200)
async def get_edificios(
        id: Optional[int] = Query(default=None, ge=1),
        nombre: Optional[str] = Query(default=None, max_length=50),
        status: Optional[bool] = Query(default=None),
        direccion: Optional[str] = Query(default=None, max_length=100),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
        response: ApiResponse[Edificios] = await edificios_service.get(
            id=id,
            nombre=nombre,
            status=status,
            direccion=direccion,
            page=page,
            page_size=page_size
        )

        return ApiResponse(msg="Edificios obtenidos correctamente", data=response['data'], pagination=response['pagination'], status_code=200)

@router.post(AppRoutes.EDIFICIOS, response_model=ApiResponse[EdificioRespuesta], status_code=201)
async def create_edificio(
        payload: EdificioCrear = Body(...),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
        edificio: Edificios = await edificios_service.create(payload)
        return ApiResponse(msg="Edificio creado", data=edificio, status_code=201)

@router.put(f"{AppRoutes.EDIFICIOS}/{{id}}", response_model=ApiResponse[EdificioRespuesta], status_code=200)
async def update_edificio(
        id: int = Path(..., ge=1),
        payload: EdificioActualizar = Body(...),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
        edificio: Edificios = await edificios_service.update(id, payload)
        return ApiResponse(msg="Edificio actualizado", data=edificio, status_code=200)

@router.delete(f"{AppRoutes.EDIFICIOS}/{{id}}", response_model=ApiResponse[EdificioRespuesta], status_code=200)
async def delete_edificio(
        id: int = Path(..., ge=1),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
        response: Edificios = await edificios_service.delete(id)
        return ApiResponse(msg="Edificio eliminado correctamente", data=response, status_code=200)

