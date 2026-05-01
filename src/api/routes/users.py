from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.controllers.users_controller import (
    activate_user_controller,
    list_users_controller,
    update_user_controller,
)
from src.db.database import get_db
from src.models.user import User
from src.schemas.user import UserActivateRequest, UserRead, UserUpdateRequest
from src.services.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[UserRead]:
    return list_users_controller(db)


@router.put("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> UserRead:
    return update_user_controller(db, id, payload)


@router.patch("/{id}/activate", response_model=UserRead, status_code=status.HTTP_200_OK)
def activate_user(
    id: int,
    payload: UserActivateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> UserRead:
    return activate_user_controller(db, id, payload)

