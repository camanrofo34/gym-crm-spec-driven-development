from sqlalchemy.orm import Session

from src.analytics.queries import get_trainer_ranking, get_user_activity_summary, get_weekly_trainer_load
from src.schemas.analytics import TrainerLoadItem, TrainerRankingItem, UserSummaryItem


def trainer_load_controller(db: Session) -> list[TrainerLoadItem]:
    return get_weekly_trainer_load(db)


def user_summary_controller(db: Session) -> list[UserSummaryItem]:
    return get_user_activity_summary(db)


def trainer_ranking_controller(db: Session) -> list[TrainerRankingItem]:
    return get_trainer_ranking(db)

