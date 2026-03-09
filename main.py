from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import processor
import security

app = FastAPI(title="Sentinel AI - Hannah Edition")


class LogEntry(BaseModel):
    ip: str
    region: str
    attempts: int


@app.get("/")
def home():
    return {"message": "Sentinel AI Engine Online", "target": "Austin_Texas_L3"}


@app.post("/analyze")
def run_analysis(logs: List[dict]):
    # Usamos el motor de procesamiento masivo
    results = processor.process_massive_data(logs)
    return results
