from datetime import date

from tests.helpers import auth_headers


def _post_activity(client, headers, user_id: int, duration: int, activity_type: str = "cardio") -> None:
    response = client.post(
        "/activities",
        json={
            "user_id": user_id,
            "duration_minutes": duration,
            "activity_type": activity_type,
            "date": date.today().isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 201


def test_analytics_endpoints_return_correct_aggregation(client) -> None:
    trainer_1, trainer_1_headers = auth_headers(client, "trainer1@example.com", "strong123", "TRAINER")
    trainer_2, trainer_2_headers = auth_headers(client, "trainer2@example.com", "strong123", "TRAINER")
    trainee_1, trainee_1_headers = auth_headers(client, "trainee1@example.com", "strong123", "TRAINEE")
    trainee_2, trainee_2_headers = auth_headers(client, "trainee2@example.com", "strong123", "TRAINEE")

    assignment_1 = client.post(
        "/assignments",
        json={"trainee_id": trainee_1["id"], "trainer_id": trainer_1["id"]},
        headers=trainer_1_headers,
    )
    assignment_2 = client.post(
        "/assignments",
        json={"trainee_id": trainee_2["id"], "trainer_id": trainer_2["id"]},
        headers=trainer_1_headers,
    )
    assert assignment_1.status_code == 201
    assert assignment_2.status_code == 201

    _post_activity(client, trainee_1_headers, trainee_1["id"], 60, "cardio")
    _post_activity(client, trainee_1_headers, trainee_1["id"], 30, "strength")
    _post_activity(client, trainee_2_headers, trainee_2["id"], 50, "cardio")

    trainer_load = client.get("/analytics/trainer-load", headers=trainer_1_headers)
    user_summary = client.get("/analytics/user-summary", headers=trainer_1_headers)
    trainer_ranking = client.get("/analytics/trainer-ranking", headers=trainer_2_headers)

    assert trainer_load.status_code == 200
    assert user_summary.status_code == 200
    assert trainer_ranking.status_code == 200

    load_by_trainer = {item["trainer_id"]: item["total_duration_minutes"] for item in trainer_load.json()}
    assert load_by_trainer[trainer_1["id"]] == 90
    assert load_by_trainer[trainer_2["id"]] == 50

    summary_by_user = {item["user_id"]: item for item in user_summary.json()}
    assert summary_by_user[trainee_1["id"]]["total_activities"] == 2
    assert summary_by_user[trainee_1["id"]]["average_duration_minutes"] == 45.0
    assert summary_by_user[trainee_2["id"]]["total_activities"] == 1

    ranking = trainer_ranking.json()
    assert ranking[0]["trainer_id"] == trainer_1["id"]
    assert ranking[0]["total_duration_minutes"] == 90
    assert ranking[1]["trainer_id"] == trainer_2["id"]

