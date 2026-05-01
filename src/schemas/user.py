from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRoleSchema(str, Enum):
    TRAINEE = "TRAINEE"
    TRAINER = "TRAINER"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleSchema
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6)
    role: UserRoleSchema | None = None


class UserActivateRequest(BaseModel):
    is_active: bool

