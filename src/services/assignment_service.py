from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.trainer_assignment import TrainerAssignment
from src.models.user import User, UserRole
from src.schemas.assignment import AssignmentCreateRequest


def create_assignment(db: Session, payload: AssignmentCreateRequest) -> TrainerAssignment:
    trainee = db.query(User).filter(User.id == payload.trainee_id).first()
    trainer = db.query(User).filter(User.id == payload.trainer_id).first()

    if trainee is None or trainer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if trainee.role != UserRole.TRAINEE or trainer.role != UserRole.TRAINER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trainer assignment must link a TRAINEE to a TRAINER",
        )

    assignment = TrainerAssignment(trainee_id=payload.trainee_id, trainer_id=payload.trainer_id)
    db.add(assignment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Assignment already exists") from exc

    db.refresh(assignment)
    return assignment


def list_assignments(db: Session) -> list[TrainerAssignment]:
    return db.query(TrainerAssignment).order_by(TrainerAssignment.id.asc()).all()

