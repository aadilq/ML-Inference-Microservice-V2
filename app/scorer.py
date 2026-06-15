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
    def score_segments(self, segments: list[dict]) -> list[dict]:
        texts = [s["text"] for s in segments]

        engagement_results = self.classifier(texts, ENGAGEMENT_LABELS)
        topic_results = self.classifier(texts, TOPIC_LABELS)
        energy_results = self.classifier(texts, ENERGY_LABELS)

        results = []
        for i, (engagement, topic, energy) in enumerate(zip(engagement_results, topic_results, energy_results)):
            results.append({
                "segment_index": i,
                "score": engagement["scores"][engagement["labels"].index("engaging highlight")],
                "topic": topic["labels"][0],
                "energy_level": energy["labels"][0].split()[0].lower()
            })
        return results
            
            



    