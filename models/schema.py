from pydantic import BaseModel, Field
from typing import Dict

class ScoreRequest(BaseModel):
    transaction_id: str
    amount: float = Field(ge=0)
    user_id: str
    f0: float
    f1: float
    f2: float
    f3: float
    f4: float
    f5: float
    f6: float
    f7: float


class ScoreResponse(BaseModel):
    fraud_score: float
    decision: str
    latency_ms: Dict[str, float]



