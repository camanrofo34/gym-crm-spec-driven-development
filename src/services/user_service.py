from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserActivateRequest, UserUpdateRequest
from src.services.security import hash_password


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def update_user(db: Session, user_id: int, payload: UserUpdateRequest) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.email is not None and payload.email != user.email:
        email_used = db.query(User).filter(User.email == payload.email).first()
        if email_used is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user.email = payload.email

    if payload.password is not None:
        user.password = hash_password(payload.password)

    if payload.role is not None:
        user.role = payload.role.value

    db.commit()
    db.refresh(user)
    return user


def set_user_active(db: Session, user_id: int, payload: UserActivateRequest) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user

