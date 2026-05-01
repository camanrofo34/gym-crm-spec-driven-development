from tests.helpers import auth_headers


def test_trainer_assignment_validation(client) -> None:
    _, headers = auth_headers(client, "manager@example.com", "strong123", "TRAINER")
    trainee, _ = auth_headers(client, "trainee1@example.com", "strong123", "TRAINEE")
    wrong_trainer, _ = auth_headers(client, "trainee2@example.com", "strong123", "TRAINEE")

    response = client.post(
        "/assignments",
        json={"trainee_id": trainee["id"], "trainer_id": wrong_trainer["id"]},
        headers=headers,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Trainer assignment must link a TRAINEE to a TRAINER"

