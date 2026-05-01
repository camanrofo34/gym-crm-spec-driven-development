from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.controllers.analytics_controller import (
    trainer_load_controller,
    trainer_ranking_controller,
    user_summary_controller,
)
from src.db.database import get_db
from src.models.user import User
from src.schemas.analytics import TrainerLoadItem, TrainerRankingItem, UserSummaryItem
from src.services.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/trainer-load", response_model=list[TrainerLoadItem], status_code=status.HTTP_200_OK)
def get_trainer_load(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[TrainerLoadItem]:
    return trainer_load_controller(db)


@router.get("/user-summary", response_model=list[UserSummaryItem], status_code=status.HTTP_200_OK)
def get_user_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[UserSummaryItem]:
    return user_summary_controller(db)


@router.get("/trainer-ranking", response_model=list[TrainerRankingItem], status_code=status.HTTP_200_OK)
def get_trainer_ranking(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[TrainerRankingItem]:
    return trainer_ranking_controller(db)

