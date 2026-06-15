from pydantic import BaseModel, HttpUrl

class ScoreRequest(BaseModel):
    url: HttpUrl

class SegmentScore(BaseModel):
    segment_index: int
    score: float
    topic: str
    energy_level: str

class ScoreResponse(BaseModel):
    scores: list[SegmentScore]
