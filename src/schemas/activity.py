from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ActivityCreateRequest(BaseModel):
    user_id: int
    duration_minutes: int = Field(gt=0)
    activity_type: str = Field(min_length=1)
    date: date

    @field_validator("date")
    @classmethod
    def date_must_not_be_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Activity date cannot be in the future")
        return value


class ActivityRead(BaseModel):
    id: int
    user_id: int
    duration_minutes: int
    activity_type: str
    date: date

    model_config = ConfigDict(from_attributes=True)

