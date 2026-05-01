from datetime import date, timedelta

from tests.helpers import auth_headers


def test_activity_creation_success(client) -> None:
    user, headers = auth_headers(client, "active@example.com", "strong123", "TRAINEE")
    response = client.post(
        "/activities",
        json={
            "user_id": user["id"],
            "duration_minutes": 45,
            "activity_type": "cardio",
            "date": date.today().isoformat(),
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["duration_minutes"] == 45


def test_activity_creation_with_invalid_date(client) -> None:
    user, headers = auth_headers(client, "future@example.com", "strong123", "TRAINEE")
    response = client.post(
        "/activities",
        json={
            "user_id": user["id"],
            "duration_minutes": 30,
            "activity_type": "strength",
            "date": (date.today() + timedelta(days=1)).isoformat(),
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_inactive_user_cannot_create_activity(client) -> None:
    user, headers = auth_headers(client, "inactive@example.com", "strong123", "TRAINEE")
    deactivate = client.patch(f"/users/{user['id']}/activate", json={"is_active": False}, headers=headers)
    response = client.post(
        "/activities",
        json={
            "user_id": user["id"],
            "duration_minutes": 30,
            "activity_type": "strength",
            "date": date.today().isoformat(),
        },
        headers=headers,
    )

    assert deactivate.status_code == 200
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive users cannot log activities"

