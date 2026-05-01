from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class UserRole(str, Enum):
    TRAINEE = "TRAINEE"
    TRAINER = "TRAINER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, native_enum=False), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC).replace(tzinfo=None),
    )

    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    trainee_assignments = relationship(
        "TrainerAssignment",
        back_populates="trainee",
        foreign_keys="TrainerAssignment.trainee_id",
        cascade="all, delete-orphan",
    )
    trainer_assignments = relationship(
        "TrainerAssignment",
        back_populates="trainer",
        foreign_keys="TrainerAssignment.trainer_id",
        cascade="all, delete-orphan",
    )
