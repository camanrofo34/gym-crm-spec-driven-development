from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.activity import Activity
from src.models.trainer_assignment import TrainerAssignment
from src.models.user import User, UserRole
from src.schemas.activity import ActivityCreateRequest


def create_activity(db: Session, payload: ActivityCreateRequest, actor: User) -> Activity:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive users cannot log activities")
    if payload.date > date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activity date cannot be in the future")
    if payload.duration_minutes <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activity duration must be greater than 0")
    if actor.id != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users can only log their own activities")

    activity = Activity(
        user_id=payload.user_id,
        duration_minutes=payload.duration_minutes,
        activity_type=payload.activity_type,
        date=payload.date,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def list_activities(db: Session, actor: User, user_id: int | None = None) -> list[Activity]:
    query = db.query(Activity)

    if actor.role == UserRole.TRAINEE:
        if user_id is not None and user_id != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Trainees can only view their own activities",
            )
        query = query.filter(Activity.user_id == actor.id)
    else:
        assigned_trainee_ids = (
            db.query(TrainerAssignment.trainee_id)
            .filter(TrainerAssignment.trainer_id == actor.id)
            .subquery()
        )
        query = query.filter(Activity.user_id.in_(assigned_trainee_ids))
        if user_id is not None:
            query = query.filter(Activity.user_id == user_id)

    return query.order_by(Activity.date.desc(), Activity.id.desc()).all()

