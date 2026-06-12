from transformers import pipeline


class Scorer:
    def __init__(self, model_name: str):
        self.classifier = pipeline(
            "zero-shot-classification",
            model=model_name
        )
