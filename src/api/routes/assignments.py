from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.controllers.assignments_controller import create_assignment_controller, list_assignments_controller
from src.db.database import get_db
from src.models.user import User
from src.schemas.assignment import AssignmentCreateRequest, AssignmentRead
from src.services.security import get_current_user

router = APIRouter(prefix="/assignments", tags=["Trainer Assignments"])


@router.post("", response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentCreateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> AssignmentRead:
    return create_assignment_controller(db, payload)


@router.get("", response_model=list[AssignmentRead], status_code=status.HTTP_200_OK)
def get_assignments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[AssignmentRead]:
    return list_assignments_controller(db)

