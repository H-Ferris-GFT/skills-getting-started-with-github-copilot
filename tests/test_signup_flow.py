import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_signup_duplicate_is_rejected():
    client = TestClient(app)

    first = client.post("/activities/Chess Club/signup?email=alice@mergington.edu")
    second = client.post("/activities/Chess Club/signup?email=alice@mergington.edu")

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student is already registered for this activity"


def test_unregister_removes_participant():
    client = TestClient(app)
    client.post("/activities/Chess Club/signup?email=bob@mergington.edu")

    response = client.delete("/activities/Chess Club/unregister?email=bob@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered bob@mergington.edu from Chess Club"

    refreshed = client.get("/activities").json()["Chess Club"]
    assert "bob@mergington.edu" not in refreshed["participants"]
