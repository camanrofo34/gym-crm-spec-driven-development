from datetime import date

from pydantic import BaseModel


class TrainerLoadItem(BaseModel):
    trainer_id: int
    trainer_email: str
    week_start: date
    week_end: date
    total_duration_minutes: int


class UserSummaryItem(BaseModel):
    user_id: int
    user_email: str
    total_activities: int
    average_duration_minutes: float


class TrainerRankingItem(BaseModel):
    rank: int
    trainer_id: int
    trainer_email: str
    total_duration_minutes: int

