import time
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
from threading import Lock
from models.schema import ScoreRequest, ScoreResponse
from logger import get_logger
from concurrent.futures import Future

logger = get_logger()
app = FastAPI()

ARTIFACT_PATH = Path("artifacts/fraud_model.joblib")

# Load at startup (module import time)
_bundle = joblib.load(ARTIFACT_PATH)
model = _bundle["model"]
feature_names = _bundle["feature_names"]


# =================
# BATCH CONFIG
# =================
BATCH_SIZE = 10
MAX_WAIT_MS = 25


queue = []
queue_lock = Lock()

@app.on_event("startup")
async def start_batch_worker():
    asyncio.create_task(batch_worker())


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/score", response_model=ScoreResponse)
async def score(req : ScoreRequest):
    t0 = time.perf_counter()

    try:
        #Preprocessing
        t1 = time.perf_counter()
        x = np.array([[getattr(req, f) for f in feature_names]], dtype = float)
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        t2 = time.perf_counter()

        #Inference
        prob = float(model.predict_proba(x)[0,1])
        t3 = time.perf_counter()

        #Decision
        decision = "approve"
        if prob >= 0.8:
            decision = "decline"
        elif prob >= 0.5:
            decision = "review"
        t4 = time.perf_counter()

    except Exception as e:
        logger.exception("scoring failed")
        raise HTTPException(status_code=500, detail="Scoring failed")

    latency = {
        "total_ms" : (t4-t0)*1000,
        "preprocess_ms": (t2 - t1) * 1000,
        "inference_ms": (t3 - t2) * 1000,
        "postprocess_ms": (t4 - t3) * 1000,
    }

    #logger.info(f"score_request | tx_id = {req.transaction_id} | f"latency= {latency})
    logger.info(f"score_request | tx_id={req.transaction_id} | "f"latency={latency}"
    )



    return ScoreResponse(fraud_score=prob, decision=decision, latency_ms=latency)