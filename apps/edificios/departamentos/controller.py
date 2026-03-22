from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from apps.edificios.departamentos.schema import DepartamentoRespuesta, DepartamentoCrear, DepartamentoActualizar
from apps.edificios.departamentos.services import DepartamentosService
from apps.edificios.models import Departamentos
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

departamentos_router = APIRouter(tags=['departamentos'])

@departamentos_router.get(AppRoutes.DEPARTAMENTOS, response_model=ApiResponse[list[DepartamentoRespuesta]], status_code=200)
async def get_departamentos(
        id: Optional[int] = Query(default=None, ge=1),
        numero_departamento: Optional[str] = Query(default=None, max_length=20),
        piso: Optional[int] = Query(default=None, ge=0, le=3),
        status: Optional[bool] = Query(default=None),
        ocupado: Optional[bool] = Query(default=None),
        edificio_id: Optional[int] = Query(default=None, ge=1),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
    try:
        response: ApiResponse[Departamentos] = await departamentos_service.get(
            id=id,
            numero_departamento=numero_departamento,
            piso=piso,
            status=status,
            ocupado=ocupado,
            edificio_id=edificio_id,
            page=page,
            page_size=page_size
        )

        return ApiResponse(msg="Departamentos obtenidos correctamente", data=response['data'], pagination=response['pagination'], status_code=200)

    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error obteniendo departamentos", "details": e.detail, "status_code": e.status_code}
        )

@departamentos_router.post(AppRoutes.DEPARTAMENTOS, response_model=ApiResponse[DepartamentoRespuesta], status_code=201)
async def create_departamento(
        payload: DepartamentoCrear,
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
    try:
        departamento: Departamentos = await departamentos_service.create(payload)
        return ApiResponse(msg="Departamento creado", data=departamento, status_code=201)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error creando departamento", "details": e.detail, "status_code": e.status_code}
        )

@departamentos_router.put(f"{AppRoutes.DEPARTAMENTOS}/{{id}}", response_model=ApiResponse[DepartamentoRespuesta], status_code=200)
async def update_departamento(
        id: int,
        payload: DepartamentoActualizar,
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
    try:
        departamento: Departamentos = await departamentos_service.update(id, payload)
        return ApiResponse(msg="Departamento actualizado", data=departamento, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error actualizando departamento", "details": e.detail, "status_code": e.status_code}
        )

@departamentos_router.delete(f"{AppRoutes.DEPARTAMENTOS}/{{id}}", response_model=ApiResponse[DepartamentoRespuesta], status_code=200)
async def delete_departamento(
        id: int,
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
    try:
        response: Departamentos = await departamentos_service.delete(id)
        return ApiResponse(msg="Departamento eliminado correctamente", data=response, status_code=200)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error eliminando departamento", "details": e.detail, "status_code": e.status_code}
        )