import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

def test_signup_and_unregister():
    # Use a test activity and email
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"

    # Signup
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code in (200, 400)  # 400 if already signed up

    # Signup again should fail
    resp_signup2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup2.status_code == 400

    # Unregister (if implemented)
    resp_unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg.status_code in (200, 404, 400)

    # Unregister again should fail
    resp_unreg2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg2.status_code in (404, 400)
