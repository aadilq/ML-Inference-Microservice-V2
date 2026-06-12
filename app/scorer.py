from transformers import pipeline

ENGAGEMENT_LABELS=["engaging highlight", "boring filler"]
TOPIC_LABELS=["action scene", "emotional moment", "comedy", "dramatic dialogue","climax", "conflict", "plot twist", "exposition"]
ENERGY_LABELS=["high energy", "medium energy", "low energy"]

class Scorer:
    def __init__(self, model_name: str):
        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name
        )
    