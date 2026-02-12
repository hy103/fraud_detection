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
    start_time = time.perf_counter()


    #Preprocessing
    t1 = time.perf_counter()
    features = np.array([[getattr(req, f) for f in feature_names]], dtype = float)
    loop = asyncio.get_event_loop()
    future = loop.create_future()


    while queue_lock :
        queue.append((features, future, start_time))

    result = await future
    return result
    
# =========================
# BATCH WORKER
# =========================
async def batch_worker():
        while True:
             await asyncio.sleep(0.005) #5ms polling

             now = time.perf_counter()
             batch = []

             with queue_lock:
                if not queue:
                    continue
                  
                #flush if size is reached
                if len(queue) >= BATCH_SIZE:
                    batch = queue[:BATCH_SIZE]
                    del queue[:BATCH_SIZE]
                elif (now- queue[0][2])*1000 >= MAX_WAIT_MS:
                     batch = queue[:]
                     queue.clear()

        if batch:
            features_batch = np.vstack([item[0] for item in batch])
            futures = [item[1] for item in batch]
            start_times = [item[2] for item in batch]
            t2 = time.perf_counter()

            preds = model.predict_proba(features_batch)[:, 1]
            t2 = time.perf_counter()

            for prob, future, start_time in zip(probs, futures, start_times):
                #Decision
                decision = "approve"
                if prob >= 0.8:
                    decision = "decline"
                elif prob >= 0.5:
                    decision = "review"
                t4 = time.perf_counter()

                latency = {
                    "total_ms" : (t4-start_time)*1000,
                    "preprocess_ms": 0 * 1000,
                    "inference_ms": (t3 - t2) * 1000/len(batch),
                    "postprocess_ms": (t4 - t3) * 1000,
                    }
                future.set_result(
            ScoreResponse(
                fraud_score=float(prob),
                decision=decision,
                latency_ms=latency
            )
        )