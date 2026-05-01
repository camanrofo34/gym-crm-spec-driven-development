from sqlalchemy.orm import Session

from src.schemas.user import UserActivateRequest, UserRead, UserUpdateRequest
from src.services.user_service import list_users, set_user_active, update_user


def list_users_controller(db: Session) -> list[UserRead]:
    users = list_users(db)
    return [UserRead.model_validate(user) for user in users]


def update_user_controller(db: Session, user_id: int, payload: UserUpdateRequest) -> UserRead:
    user = update_user(db, user_id, payload)
    return UserRead.model_validate(user)


def activate_user_controller(db: Session, user_id: int, payload: UserActivateRequest) -> UserRead:
    user = set_user_active(db, user_id, payload)
    return UserRead.model_validate(user)

