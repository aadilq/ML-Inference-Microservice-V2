from unittest.mock import patch, MagicMock
from app.scorer import Scorer

def test_score_mapping():
    with patch("app.scorer.pipeline") as mock_pipeline:
        mock_classifer = MagicMock()
        mock_pipeline.return_value = mock_classifer
        mock_classifer.side_effect = [
            [{
                "labels": ["engaging highlight", "boring filler"],
                "scores": [0.87, 0.13]
            }],
            [{
                "labels": ["climax", "action scene", "emotional moment", "comedy", "dramatic dialogue", "conflict", "plot twist", "exposition"],
                "scores": [0.91, 0.78, 0.65, 0.54, 0.42, 0.31, 0.23, 0.09]          
            }],
            [{
                "labels": ["high energy", "medium energy", "low energy"],
                "scores": [0.89, 0.54, 0.12]            
            }]
        ]
        scorer = Scorer("fake-model")
        result = scorer.score_segments([{"text": "I can't. Ah, I knew it!", "start": 1.09, "end": 1.16, "speaker": "Speaker A"}])

        assert result[0]["score"] == 0.87
        assert result[0]["topic"] == "climax"
        assert result[0]["energy_level"] == "high"