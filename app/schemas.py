from pydantic import BaseModel, HttpUrl, field_validator

class ScoreRequest(BaseModel):
    url: HttpUrl


    @field_validator("url")
    @classmethod
    def must_be_youtube(cls, v):
        if "youtube.com" not in str(v) and "youtu.be" not in str(v):
            raise ValueError("URL must be a Youtube link")
        return v

class SegmentScore(BaseModel):
    segment_index: int
    score: float
    topic: str
    energy_level: str
    raw_text: str

class ScoreResponse(BaseModel):
    scores: list[SegmentScore]
