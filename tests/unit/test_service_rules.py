from datetime import date

import pytest
from fastapi import HTTPException

from src.models.user import User
from src.schemas.activity import ActivityCreateRequest
from src.schemas.assignment import AssignmentCreateRequest
from src.services.activity_service import create_activity
from src.services.assignment_service import create_assignment
from src.services.security import hash_password


def test_create_assignment_requires_trainee_to_trainer(db_session) -> None:
    trainee_a = User(email="t1@example.com", password=hash_password("secret123"), role="TRAINEE")
    trainee_b = User(email="t2@example.com", password=hash_password("secret123"), role="TRAINEE")
    db_session.add_all([trainee_a, trainee_b])
    db_session.commit()
    db_session.refresh(trainee_a)
    db_session.refresh(trainee_b)

    with pytest.raises(HTTPException) as exc:
        create_assignment(
            db_session,
            AssignmentCreateRequest(trainee_id=trainee_a.id, trainer_id=trainee_b.id),
        )

    assert exc.value.status_code == 400


def test_inactive_user_cannot_create_activity(db_session) -> None:
    inactive_user = User(
        email="inactive@unit.com",
        password=hash_password("secret123"),
        role="TRAINEE",
        is_active=False,
    )
    db_session.add(inactive_user)
    db_session.commit()
    db_session.refresh(inactive_user)

    with pytest.raises(HTTPException) as exc:
        create_activity(
            db_session,
            ActivityCreateRequest(
                user_id=inactive_user.id,
                duration_minutes=20,
                activity_type="cardio",
                date=date.today(),
            ),
            actor=inactive_user,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Inactive users cannot log activities"


def test_user_cannot_log_activity_for_another_user(db_session) -> None:
    user_a = User(email="a@unit.com", password=hash_password("secret123"), role="TRAINEE")
    user_b = User(email="b@unit.com", password=hash_password("secret123"), role="TRAINEE")
    db_session.add_all([user_a, user_b])
    db_session.commit()
    db_session.refresh(user_a)
    db_session.refresh(user_b)

    with pytest.raises(HTTPException) as exc:
        create_activity(
            db_session,
            ActivityCreateRequest(
                user_id=user_b.id,
                duration_minutes=25,
                activity_type="strength",
                date=date.today(),
            ),
            actor=user_a,
        )

    assert exc.value.status_code == 403

