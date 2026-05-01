from tests.helpers import login_user, register_user


def test_successful_user_registration(client) -> None:
    response = client.post(
        "/auth/register",
        json={"email": "trainee@example.com", "password": "strong123", "role": "TRAINEE"},
    )
    body = response.json()

    assert response.status_code == 201
    assert body["user"]["email"] == "trainee@example.com"
    assert body["user"]["role"] == "TRAINEE"
    assert "access_token" in body


def test_duplicate_email_rejection(client) -> None:
    register_user(client, "duplicate@example.com", "strong123", "TRAINEE")
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "strong123", "role": "TRAINER"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_login_success_and_failure(client) -> None:
    register_user(client, "login@example.com", "strong123", "TRAINER")
    ok = login_user(client, "login@example.com", "strong123")
    fail = client.post("/auth/login", json={"email": "login@example.com", "password": "wrong123"})

    assert "access_token" in ok
    assert fail.status_code == 401
    assert fail.json()["detail"] == "Invalid credentials"

