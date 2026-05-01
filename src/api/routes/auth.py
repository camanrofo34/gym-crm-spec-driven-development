from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.controllers.auth_controller import login_controller, register_controller
from src.db.database import get_db
from src.schemas.auth import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return register_controller(db, payload)


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return login_controller(db, payload)

