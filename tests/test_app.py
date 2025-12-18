from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball Club" in data


def test_signup_and_remove_participant():
    activity = "Basketball Club"
    email = "test.user@example.com"

    # Ensure test email is not present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Remove
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
