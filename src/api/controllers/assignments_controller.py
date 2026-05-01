from sqlalchemy.orm import Session

from src.schemas.assignment import AssignmentCreateRequest, AssignmentRead
from src.services.assignment_service import create_assignment, list_assignments


def create_assignment_controller(db: Session, payload: AssignmentCreateRequest) -> AssignmentRead:
    assignment = create_assignment(db, payload)
    return AssignmentRead.model_validate(assignment)


def list_assignments_controller(db: Session) -> list[AssignmentRead]:
    assignments = list_assignments(db)
    return [AssignmentRead.model_validate(assignment) for assignment in assignments]

