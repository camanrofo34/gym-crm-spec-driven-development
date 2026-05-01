from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class TrainerAssignment(Base):
    __tablename__ = "trainer_assignments"
    __table_args__ = (UniqueConstraint("trainee_id", "trainer_id", name="uq_trainee_trainer"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trainee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    trainee = relationship("User", back_populates="trainee_assignments", foreign_keys=[trainee_id])
    trainer = relationship("User", back_populates="trainer_assignments", foreign_keys=[trainer_id])

