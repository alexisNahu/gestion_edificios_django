from django.contrib.auth.models import User
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from apps.authentication.schema import LoginResponse, LoginRequest, RegisterRequest, UserPyantic
from apps.authentication.service import AuthService
from core.exceptions import ApiError
from core.routes import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=["authentication"])

@router.post(AppRoutes.LOGIN, response_model=ApiResponse[LoginResponse], status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, auth_service: AuthService = Depends(AuthService)):
    try:
        response: LoginResponse = await auth_service.login(username=request.username, password=request.password)
        return ApiResponse(msg="Usuario logeado correctamente", data=response, status_code=status.HTTP_200_OK)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error logeando", "details": e.detail, "status_code": e.status_code}
        )


@router.post(AppRoutes.REGISTER, response_model=ApiResponse[UserPyantic], status_code=status.HTTP_200_OK)
async def register(request: RegisterRequest, auth_service: AuthService=Depends(AuthService)):
    try:
        response: User = await auth_service.register(email=request.email, username=request.username, password=request.password)
        return ApiResponse(msg="Usuario registrado correctamente", data=response, status_code=status.HTTP_200_OK)
    except ApiError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"msg": "Error registrando al usuario "+request.username, "details": e.detail, "status_code": e.status_code}
        )


