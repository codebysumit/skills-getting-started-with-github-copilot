import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    test_client = TestClient(app)

    yield test_client

    # Restore app state after each test
    activities["Chess Club"]["participants"] = original_participants


def test_delete_participant_removes_student_from_activity(client):
    # Arrange
    email = "michael@mergington.edu"
    assert email in activities["Chess Club"]["participants"]

    # Act
    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"


def test_delete_nonexistent_participant_returns_404(client):
    # Arrange
    email = "missing@mergington.edu"
    assert email not in activities["Chess Club"]["participants"]

    # Act
    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
