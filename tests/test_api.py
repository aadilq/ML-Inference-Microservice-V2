from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.database import get_db

mock_db = MagicMock()
app.dependency_overrides[get_db] = lambda: mock_db



@patch("app.main.download_video")
@patch("app.main.transcribe_video")
@patch("app.main.Scorer")
@patch("app.main.init_db")
@patch("app.main.shutil.rmtree")
def test_score_endpoint(mock_rmtree, mock_init_db, mock_scorer, mock_transcribe, mock_download):
    mock_download.return_value = "/tmp/fakedir/source.mp4"
    mock_transcribe.return_value = [{"text": "test segment", "start": 0.0, "end":
    1.0, "speaker": "A"}]
    mock_scorer.return_value.score_segments.return_value = [
        {"segment_index": 0, "score": 0.87, "topic": "climax", "energy_level":
  "high", "raw_text": "test segment"}]
    
    with TestClient(app=app) as client:
        response = client.post("/score", json={"url":"https://www.youtube.com/watch?v=test"})
        assert response.status_code == 200
        assert response.json() == {
        "scores": [
            {"segment_index": 0, "score": 0.87, "topic": "climax", "energy_level":
    "high", "raw_text": "test segment"}
        ]
        }


@patch("app.main.init_db")
@patch("app.main.Scorer")
def test_health_endpoint(mock_scorer, mock_init_db):
    with TestClient(app=app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert "model" in response.json()