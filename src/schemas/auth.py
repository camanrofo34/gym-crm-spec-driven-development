from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas.user import UserRead, UserRoleSchema


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRoleSchema


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

    model_config = ConfigDict(from_attributes=True)

