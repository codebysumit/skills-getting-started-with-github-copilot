from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_student_from_activity():
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in client.get("/activities").json()["Chess Club"]["participants"]

    # restore state for the rest of the test session
    client.post("/activities/Chess Club/signup?email=michael@mergington.edu")


def test_delete_nonexistent_participant_returns_404():
    response = client.delete("/activities/Chess Club/signup?email=missing@mergington.edu")

    assert response.status_code == 404
