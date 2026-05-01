from fastapi.testclient import TestClient


def register_user(client: TestClient, email: str, password: str, role: str) -> dict:
    response = client.post(
        "/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    assert response.status_code == 201
    return response.json()


def login_user(client: TestClient, email: str, password: str) -> dict:
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()


def auth_headers(client: TestClient, email: str, password: str, role: str) -> tuple[dict, dict]:
    register_payload = register_user(client, email, password, role)
    login_payload = login_user(client, email, password)
    return register_payload["user"], {"Authorization": f"Bearer {login_payload['access_token']}"}

