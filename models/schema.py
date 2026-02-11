from pydantic import BaseModel, Field

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
    latency_ms: dict



31,636  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615079.07394975, 'preprocess_ms': 0.0045000051613897085, 'inference_ms': 0.09841698920354247, 'postprocess_ms': 0.0002500019036233425}
INFO:     127.0.0.1:58691 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,638  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615080.9606308, 'preprocess_ms': 0.005209003575146198, 'inference_ms': 0.11104097939096391, 'postprocess_ms': 0.00029199873097240925}
INFO:     127.0.0.1:58692 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,640  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615083.02257285, 'preprocess_ms': 0.004750007065013051, 'inference_ms': 0.10549998842179775, 'postprocess_ms': 0.0002910092007368803}
INFO:     127.0.0.1:58693 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,642  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615084.96942177, 'preprocess_ms': 0.004458997864276171, 'inference_ms': 0.10004101204685867, 'postprocess_ms': 0.00029199873097240925}
INFO:     127.0.0.1:58694 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,644  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615086.94346002, 'preprocess_ms': 0.006624992238357663, 'inference_ms': 0.12462501763366163, 'postprocess_ms': 0.0002500019036233425}
INFO:     127.0.0.1:58695 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,646  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615088.7900455, 'preprocess_ms': 0.004917004844173789, 'inference_ms': 0.10937501792795956, 'postprocess_ms': 0.0002500019036233425}
INFO:     127.0.0.1:58696 - "POST /score HTTP/1.1" 200 OK
2026-02-09 17:48:31,648  | (levelname)s | score_request | tx_id=tx123 | latency={'total_ms': -178615090.6522311, 'preprocess_ms': 0.0045000051613897085, 'inference_ms': 0.10216599912382662, 'postprocess_ms': 0.0002500019036233425}
INFO:     127.0.0.1:58697 - "POST /score HTTP/1.1" 200 OK