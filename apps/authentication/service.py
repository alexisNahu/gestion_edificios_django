from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from apps.authentication.jwt_service import JWTService
from django.conf import settings

from apps.authentication.schema import LoginResponse
from core.exceptions import UnauthorizedError, ConflictError
from core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


class AuthService:
    def __init__(self):
        self.jwtService = JWTService()


    async def login(self, username: str, password: str) -> LoginResponse:
        user = await sync_to_async(authenticate)(username=username, password=password)

        if not user: raise UnauthorizedError("Credenciales Invalidas")

        token = self.jwtService.generate_token(user, ACCESS_TOKEN_EXPIRE_MINUTES, settings.SECRET_KEY)
        refresh_token = self.jwtService.generate_token(user, REFRESH_TOKEN_EXPIRE_MINUTES, settings.SECRET_REFRESH_KEY)

        return LoginResponse(access_token=token, refresh_token=refresh_token, token_type="bearer")

    @staticmethod
    async def register(email: str, password: str, username: str) -> User:
        username_exists: bool = await sync_to_async(User.objects.filter(username=username).exists)()
        email_exists: bool = await sync_to_async(User.objects.filter(email=email).exists)()

        if username_exists: raise ConflictError('Ya existe un usuario con el username '+username)
        if email_exists: raise ConflictError('Ya existe un ese email '+email)

        new_user: User = await sync_to_async(User.objects.create_user)(username, email, password)

        return new_user


