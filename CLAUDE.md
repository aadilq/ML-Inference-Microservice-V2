# ML Inference Microservice

## Project Goal

A standalone synchronous FastAPI service that accepts a YouTube URL, downloads the video, transcribes it via AssemblyAI, and scores each transcript segment for engagement potential using HuggingFace Zero-Shot Classification (`facebook/bart-large-mnli`). Inference results are persisted to PostgreSQL and returned to the caller in the same scored-segment shape as the V1 Claude API output. Designed to demonstrate ML model integration into a production pipeline with a focus on low-latency inference.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Video download | yt-dlp |
| Transcription | AssemblyAI (speaker diarization + timestamped segments) |
| ML Model | HuggingFace Transformers (`facebook/bart-large-mnli`) |
| Inference type | Zero-Shot Classification |
| Database | PostgreSQL (via SQLAlchemy) |
| Containerization | Docker Compose |
| Testing | pytest |

---

## Architecture

```
Client
  │
  ▼
FastAPI (port 8001)
  ├── POST /score   → accepts YouTube URL, runs full pipeline, returns scores
  └── GET  /health  → returns service status + loaded model name
  │
  ▼ (synchronous pipeline — request blocks until complete)
yt-dlp
  └── downloads video to temp directory
  │
  ▼
AssemblyAI
  └── transcribes audio → timestamped segments with speaker labels
  │
  ▼
HuggingFace Pipeline (loaded once at startup via FastAPI lifespan)
  └── facebook/bart-large-mnli (zero-shot classification)
        ├── Engagement labels → derives score (0.0 – 1.0)
        ├── Topic labels      → derives topic string
        └── Energy labels     → derives energy_level
  │
  ▼
PostgreSQL
  ├── inference_requests table  — one record per POST /score call
  └── inference_results table   — one record per scored segment
```

---

## Data Flow

1. Client sends `POST /score` with a YouTube URL
2. yt-dlp downloads the video to a temp directory
3. AssemblyAI transcribes audio and returns timestamped utterances with speaker labels
4. Segments are passed to the HuggingFace scorer (model already loaded in memory)
5. Zero-shot classification runs across three label groups per segment (batched)
6. An `InferenceRequest` record is written to PostgreSQL
7. One `InferenceResult` record written per segment
8. Temp video file deleted; scores returned to client
9. Client receives scored segments in the same shape as V1 Claude output

---

## Input / Output

### Input

```json
{ "url": "https://www.youtube.com/watch?v=..." }
```

### Output (same shape as V1 Claude response)

```json
{
  "scores": [
    { "segment_index": 0, "score": 0.91, "topic": "climax", "energy_level": "high" }
  ]
}
```

---

## Label Groups (Zero-Shot Classification)

```
Engagement  →  ["engaging highlight", "boring filler"]
Topic       →  ["action scene", "emotional moment", "comedy", "dramatic dialogue",
                "climax", "conflict", "plot twist", "exposition"]
Energy      →  ["high energy", "medium energy", "low energy"]
```

`score` is the `"engaging highlight"` entailment probability (0.0 – 1.0).
`topic` is the highest-scoring topic label.
`energy_level` is the first word of the highest-scoring energy label (`"high"`, `"medium"`, or `"low"`).

---

## Database Schema

### inference_requests

```
request_id     UUID       (PK)
url            string
model_name     string
segment_count  integer
created_at     timestamp
```

### inference_results

```
result_id      UUID       (PK)
request_id     FK → inference_requests
segment_index  integer
raw_text       string
score          float      (0.0 – 1.0)
topic          string
energy_level   string     ("low" | "medium" | "high")
created_at     timestamp
```

---

## Environment Variables

```
DATABASE_URL=postgresql://user:password@db:5432/inference
ASSEMBLYAI_API_KEY=your_key_here
HF_MODEL=facebook/bart-large-mnli
```

---

## Build Roadmap

### Phase 1 — Project Scaffold
- [✅] **1.1** Write `requirements.txt` with all dependencies
- [✅] **1.2** Write `.gitignore` and `.env.example`
- [✅] **1.3** Write `docker-compose.yml` skeleton with `api` and `db` services

### Phase 2 — Database Layer
- [✅] **2.1** Write `database.py` — engine, `SessionLocal`, and `create_all` helper
- [✅] **2.2** Write `models.py` — `InferenceRequest` and `InferenceResult` SQLAlchemy models
- [ ] **2.3** Verify DB connection and table creation fires correctly on app startup

### Phase 3 — Download Step
- [ ] **3.1** Integrate `yt-dlp` to download video from a YouTube URL to a temp directory
- [ ] **3.2** Add YouTube URL validation (format check + domain check)
- [ ] **3.3** Handle download errors cleanly (raise HTTP exception with clear message)

### Phase 4 — Transcription Step
- [ ] **4.1** Integrate AssemblyAI SDK with speaker diarization enabled
- [ ] **4.2** Parse response into a list of segments: `text`, `start`, `end`, `speaker`
- [ ] **4.3** Handle transcription errors cleanly

### Phase 5 — ML Scorer
- [ ] **5.1** Write `scorer.py` — `Scorer` class, load `facebook/bart-large-mnli` pipeline in `__init__`
- [ ] **5.2** Define the three candidate label groups as module-level constants
- [ ] **5.3** Implement `score_segments()` — batched zero-shot classification across all label groups
- [ ] **5.4** Map raw classification output → `score` (float), `topic` (string), `energy_level` (string)

### Phase 6 — API Layer
- [ ] **6.1** Write `schemas.py` — `ScoreRequest`, `SegmentScore`, `ScoreResponse` Pydantic models
- [ ] **6.2** Write `main.py` — FastAPI app with lifespan (model load + DB init) and DB session dependency
- [ ] **6.3** Implement `POST /score` — validate URL, run pipeline (download → transcribe → score), persist to DB, delete temp file, return response
- [ ] **6.4** Implement `GET /health` — return `{ "status": "ok", "model": "<HF_MODEL>" }`

### Phase 7 — Containerization
- [ ] **7.1** Write `Dockerfile` — install deps with CPU-only torch index URL, pre-download HF model at build time
- [ ] **7.2** Wire `docker-compose.yml` — env vars, `db` health check, `api` depends-on db
- [ ] **7.3** Smoke test: `docker compose up --build`, hit `GET /health` then `POST /score` with a real YouTube URL

### Phase 8 — Testing
- [ ] **8.1** Write `test_scorer.py` — unit tests with mocked HF pipeline, verify score/topic/energy mapping logic
- [ ] **8.2** Write `test_api.py` — integration test for `POST /score`: assert response shape and DB rows written
- [ ] **8.3** Add `GET /health` integration test — assert `model` field present in response
- [ ] **8.4** Run full test suite (`pytest`), confirm all tests pass
