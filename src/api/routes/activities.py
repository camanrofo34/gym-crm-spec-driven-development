from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.controllers.activities_controller import create_activity_controller, list_activities_controller
from src.db.database import get_db
from src.models.user import User
from src.schemas.activity import ActivityCreateRequest, ActivityRead
from src.services.security import get_current_user

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ActivityRead:
    return create_activity_controller(db, payload, current_user)


@router.get("", response_model=list[ActivityRead], status_code=status.HTTP_200_OK)
def get_activities(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ActivityRead]:
    return list_activities_controller(db, current_user, user_id=user_id)

