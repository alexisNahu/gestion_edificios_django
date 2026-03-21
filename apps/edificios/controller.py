from fastapi import APIRouter, Depends, HTTPException

from apps.edificios.schema import EdificioFiltros, EdificioRespuesta, EdificioCrear
from apps.edificios.services import EdificiosService
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=['edificios'])

@router.get(AppRoutes.EDIFICIOS, response_model=ApiResponse[list[EdificioRespuesta]], status_code=200)
async def get_edificios(
        filtros: EdificioFiltros = Depends(EdificioFiltros),
        edificios_service: EdificiosService = Depends(EdificiosService)
):
    try:
        edificios = await edificios_service.get_edificios(filtros)
        return ApiResponse(msg="Edificios obtenidos correctamente", data=edificios, status_code=200)
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

        edificio = await edificios_service.create_edificio(payload)
        return ApiResponse(msg="Edificio creado", data=edificio, status_code=201)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error creando edificios", "details": e.detail, "status_code": e.status_code}
        )