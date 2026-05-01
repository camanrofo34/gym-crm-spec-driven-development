from sqlalchemy.orm import Session

from src.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from src.schemas.user import UserRead
from src.services.auth_service import login_user, register_user


def register_controller(db: Session, payload: RegisterRequest) -> AuthResponse:
    user = register_user(db, payload)
    token, logged_user = login_user(db, LoginRequest(email=payload.email, password=payload.password))
    return AuthResponse(access_token=token, user=UserRead.model_validate(logged_user))


def login_controller(db: Session, payload: LoginRequest) -> AuthResponse:
    token, user = login_user(db, payload)
    return AuthResponse(access_token=token, user=UserRead.model_validate(user))

