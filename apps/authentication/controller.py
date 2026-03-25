from django.contrib.auth.models import User
from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status

from apps.authentication.schema import LoginResponse, LoginRequest, RegisterRequest, UserPyantic
from apps.authentication.service import AuthService
from core.constants import AppRoutes
from core.schemas import ApiResponse

router = APIRouter(tags=["authentication"])

@router.post(AppRoutes.LOGIN, response_model=ApiResponse[LoginResponse], status_code=status.HTTP_200_OK)
async def login(request: LoginRequest = Body(...), auth_service: AuthService = Depends(AuthService)):
        response: LoginResponse = await auth_service.login(username=request.username, password=request.password.get_secret_value())
        return ApiResponse(msg="Usuario logeado correctamente", data=response, status_code=status.HTTP_200_OK)


@router.post(AppRoutes.REGISTER, response_model=ApiResponse[UserPyantic], status_code=status.HTTP_200_OK)
async def register(request: RegisterRequest = Body(...), auth_service: AuthService=Depends(AuthService)):
        response: User = await auth_service.register(email=request.email, username=request.username, password=request.password.get_secret_value())
        return ApiResponse(msg="Usuario registrado correctamente", data=response, status_code=status.HTTP_200_OK)


