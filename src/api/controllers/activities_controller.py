from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.activity import ActivityCreateRequest, ActivityRead
from src.services.activity_service import create_activity, list_activities


def create_activity_controller(db: Session, payload: ActivityCreateRequest, actor: User) -> ActivityRead:
    activity = create_activity(db, payload, actor)
    return ActivityRead.model_validate(activity)


def list_activities_controller(db: Session, actor: User, user_id: int | None = None) -> list[ActivityRead]:
    activities = list_activities(db, actor, user_id=user_id)
    return [ActivityRead.model_validate(activity) for activity in activities]

