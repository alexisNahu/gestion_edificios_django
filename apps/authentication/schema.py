from datetime import datetime
from typing import Annotated

from django.forms import EmailField
from pydantic import BaseModel, EmailStr, Field, SecretStr

class UserPyantic(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # permite crear desde modelo Django

class TokenPayload(BaseModel):
    id: int
    username: str
    email: EmailStr
    exp: datetime

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    password: str = Annotated[SecretStr, Field(min_length=8, max_length=100)]

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = EmailStr
    password: str = Annotated[SecretStr, Field(min_length=8, max_length=100)]
