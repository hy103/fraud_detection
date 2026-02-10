import time
from pathlib import Path
from fastapi import FastAPI
import joblib
import numpy as np
from models.schema import ScoreRequest, ScoreResponse


app = FastAPI()

ARTIFACT_PATH = Path("artifacts/fraud_model.joblib")

# Load at startup (module import time)
_bundle = joblib.load(ARTIFACT_PATH)
model = _bundle["model"]
feature_names = _bundle["feature_names"]

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/score", response_model=ScoreResponse)
def score(req : ScoreRequest):
    t0 = time.perf_counter()

    x = np.array([[getattr(req, f) for f in feature_names]], dtype = float)

    prob = float(model.predict_proba(x)[0,1])

    decision = "approve"
    if prob >= 0.8:
        decision = "decline"
    elif prob >= 0.5:
        decision = "review"

    latency_ms = int((time.perf_counter() - t0) * 1000)

    return ScoreResponse(fraud_score=prob, decision=decision, latency_ms=latency_ms)