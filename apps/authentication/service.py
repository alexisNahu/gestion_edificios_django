from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from apps.authentication.jwt_service import JWTService
from django.conf import settings

from apps.authentication.schema import LoginResponse
from core.exceptions import UnauthorizedError, ConflictError


class AuthService:
    def __init__(self):
        self.jwtService = JWTService()


    async def login(self, username: str, password: str) -> LoginResponse:
        user = await sync_to_async(authenticate)(username=username, password=password)

        if not user: raise UnauthorizedError("Credenciales Invalidas")

        token = self.jwtService.generate_token(user, 1, settings.SECRET_KEY)
        refresh_token = self.jwtService.generate_token(user, 4, settings.SECRET_REFRESH_KEY)

        return LoginResponse(access_token=token, refresh_token=refresh_token, token_type="bearer")

    @staticmethod
    async def register(email: str, password: str, username: str) -> User:
        email_exists: bool = await sync_to_async(User.objects.filter(email=email).exists)()

        if email_exists: raise ConflictError('Ya existe una cuenta asociada a ese correo '+email)

        new_user: User = await sync_to_async(User.objects.create_user)(username, email, password)

        return new_user


