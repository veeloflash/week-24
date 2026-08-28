from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def login(username, password):
    response = client.post(
        "/api/users/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()


def test_login_token_authentication_and_ownership():
    student_a = login("ming", "123")
    student_b = login("tao", "123")

    own = client.get(
        f"/api/progress/{student_a['user_id']}",
        headers={"token": student_a["token"]},
    )
    other = client.get(
        f"/api/progress/{student_b['user_id']}",
        headers={"token": student_a["token"]},
    )
    invalid_token = client.get(
        f"/api/progress/{student_a['user_id']}",
        headers={"token": "invalid-token"},
    )

    assert own.status_code == 200
    assert other.status_code == 403
    assert invalid_token.status_code == 401
