import runpy
import sys
from pathlib import Path
from unittest.mock import patch

app_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(app_path))

from app import app


def test_app_starts_uvicorn_when_run_directly():
    app_file = app_path / "app.py"

    with patch("uvicorn.run") as mock_run:
        runpy.run_path(str(app_file), run_name="__main__")

    mock_run.assert_called_once()
