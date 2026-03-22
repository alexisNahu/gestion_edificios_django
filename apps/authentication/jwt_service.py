from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from jose import jwt
from django.conf import settings
from apps.authentication.schema import TokenPayload

class JWTService:
    @staticmethod
    def generate_token(user: User, expires_in: int = 1, secret: str = settings.SECRET_KEY) -> str:
        payload = TokenPayload(
            id=user.pk,
            username=user.username,
            email=user.email,
            exp= datetime.now(timezone.utc) + timedelta(hours=expires_in),
        )
        to_encode = payload.model_dump()

        return jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)