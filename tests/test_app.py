import runpy
import sys
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

app_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(app_path))

from app import app


def test_app_starts_uvicorn_when_run_directly():
    app_file = app_path / "app.py"

    with patch("uvicorn.run") as mock_run:
        runpy.run_path(str(app_file), run_name="__main__")

    mock_run.assert_called_once()


def test_student_cannot_register_twice_for_same_activity():
    client = TestClient(app)

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already registered for this activity"
