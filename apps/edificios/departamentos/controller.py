from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path

from apps.edificios.departamentos.schema import DepartamentoRespuesta, DepartamentoCrear, DepartamentoActualizar
from apps.edificios.departamentos.services import DepartamentosService
from apps.edificios.models import Departamentos
from core.constants import AppRoutes
from core.exceptions import ApiError
from core.schemas import ApiResponse

router = APIRouter(tags=['departamentos'])

@router.get(AppRoutes.DEPARTAMENTOS, response_model=ApiResponse[list[DepartamentoRespuesta]], status_code=200)
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

@router.post(AppRoutes.DEPARTAMENTOS, response_model=ApiResponse[DepartamentoRespuesta], status_code=201)
async def create_departamento(
        payload: DepartamentoCrear = Body(...),
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
        departamento: Departamentos = await departamentos_service.create(payload)
        return ApiResponse(msg="Departamento creado", data=departamento, status_code=201)

@router.put(f"{AppRoutes.DEPARTAMENTOS}/{{id}}", response_model=ApiResponse[DepartamentoRespuesta], status_code=200)
async def update_departamento(
        id: int = Path(..., ge=1),
        payload: DepartamentoActualizar = Body(...),
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
        departamento: Departamentos = await departamentos_service.update(id, payload)
        return ApiResponse(msg="Departamento actualizado", data=departamento, status_code=200)

@router.delete(f"{AppRoutes.DEPARTAMENTOS}/{{id}}", response_model=ApiResponse[DepartamentoRespuesta], status_code=200)
async def delete_departamento(
        id: int = Path(..., ge=1),
        departamentos_service: DepartamentosService = Depends(DepartamentosService)
):
        response: Departamentos = await departamentos_service.delete(id)
        return ApiResponse(msg="Departamento eliminado correctamente", data=response, status_code=200)
