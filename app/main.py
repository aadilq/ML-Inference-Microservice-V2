from fastapi import FastAPI, Depends, Request, HTTPException
from contextlib import asynccontextmanager
from app.database import init_db, get_db
from sqlalchemy.orm import Session
from app.scorer import Scorer
import os
from dotenv import load_dotenv
from app.schemas import ScoreRequest, ScoreResponse
from app.downloader import download_video
from app.transcriber import transcribe_video
from app.models import Request as InferenceRequest, Result as InferenceResult
import shutil

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up...")
    init_db()
    app.state.clipscorer = Scorer(os.getenv("HF_MODEL"))
    yield
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post('/score')
def score(body: ScoreRequest, request: Request, db: Session = Depends(get_db)):
    video_url = str(body.url)
    source_path = None
    try:
        source_path = download_video(video_url)
        segments = transcribe_video(source_path)
        scores = request.app.state.clipscorer.score_segments(segments)
        inferenceRequest = InferenceRequest(video_url=video_url, model_name=os.getenv("HF_MODEL"), segment_count=len(segments))
        db.add(inferenceRequest)
        db.commit()
        db.refresh(inferenceRequest)

        for segment, score in zip(segments, scores):
            inferenceResult = InferenceResult(request_id=inferenceRequest.request_id, segment_index=score["segment_index"], raw_text=segment["text"], score=score["score"], topic=score["topic"], energy_level=score["energy_level"])
            db.add(inferenceResult)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if source_path:
            shutil.rmtree(os.path.dirname(source_path))
    return ScoreResponse(scores=scores)

@app.get('/health')
def healthcheck():
    return {"status": "ok", "model": os.getenv("HF_MODEL")}


    


