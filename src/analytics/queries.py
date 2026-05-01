from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from src.models.activity import Activity
from src.models.trainer_assignment import TrainerAssignment
from src.models.user import User
from src.schemas.analytics import TrainerLoadItem, TrainerRankingItem, UserSummaryItem


def get_weekly_trainer_load(db: Session) -> list[TrainerLoadItem]:
    trainer = aliased(User)
    week_key = func.strftime("%Y-%W", Activity.date)

    rows = (
        db.query(
            TrainerAssignment.trainer_id,
            trainer.email.label("trainer_email"),
            week_key.label("week_key"),
            func.sum(Activity.duration_minutes).label("total_duration_minutes"),
        )
        .join(Activity, Activity.user_id == TrainerAssignment.trainee_id)
        .join(trainer, trainer.id == TrainerAssignment.trainer_id)
        .group_by(TrainerAssignment.trainer_id, trainer.email, week_key)
        .order_by(TrainerAssignment.trainer_id.asc(), week_key.asc())
        .all()
    )

    result: list[TrainerLoadItem] = []
    for row in rows:
        week_start = datetime.strptime(f"{row.week_key}-1", "%Y-%W-%w").date()
        week_end = week_start + timedelta(days=6)
        result.append(
            TrainerLoadItem(
                trainer_id=row.trainer_id,
                trainer_email=row.trainer_email,
                week_start=week_start,
                week_end=week_end,
                total_duration_minutes=int(row.total_duration_minutes or 0),
            )
        )
    return result


def get_user_activity_summary(db: Session) -> list[UserSummaryItem]:
    rows = (
        db.query(
            User.id.label("user_id"),
            User.email.label("user_email"),
            func.count(Activity.id).label("total_activities"),
            func.coalesce(func.avg(Activity.duration_minutes), 0).label("average_duration_minutes"),
        )
        .outerjoin(Activity, Activity.user_id == User.id)
        .group_by(User.id, User.email)
        .order_by(User.id.asc())
        .all()
    )

    return [
        UserSummaryItem(
            user_id=row.user_id,
            user_email=row.user_email,
            total_activities=int(row.total_activities),
            average_duration_minutes=float(row.average_duration_minutes),
        )
        for row in rows
    ]


def get_trainer_ranking(db: Session) -> list[TrainerRankingItem]:
    trainer = aliased(User)
    rows = (
        db.query(
            TrainerAssignment.trainer_id,
            trainer.email.label("trainer_email"),
            func.sum(Activity.duration_minutes).label("total_duration_minutes"),
        )
        .join(Activity, Activity.user_id == TrainerAssignment.trainee_id)
        .join(trainer, trainer.id == TrainerAssignment.trainer_id)
        .group_by(TrainerAssignment.trainer_id, trainer.email)
        .order_by(func.sum(Activity.duration_minutes).desc(), TrainerAssignment.trainer_id.asc())
        .all()
    )

    ranking: list[TrainerRankingItem] = []
    for index, row in enumerate(rows, start=1):
        ranking.append(
            TrainerRankingItem(
                rank=index,
                trainer_id=row.trainer_id,
                trainer_email=row.trainer_email,
                total_duration_minutes=int(row.total_duration_minutes or 0),
            )
        )
    return ranking

