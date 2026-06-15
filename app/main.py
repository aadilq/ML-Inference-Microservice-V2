from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.scorer import Scorer
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up...")
    init_db()
    app.state.clipscorer = Scorer(os.getenv("HF_MODEL"))
    yield
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)