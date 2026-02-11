import time
import requests
import statistics

URL = "http://127.0.0.1:8000/score"

payload = {
    "transaction_id": "tx123",
    "user_id": "u1",
    "amount": 1200,
    "f0": 0.1, "f1": 0.2, "f2": 0.3, "f3": 0.4,
    "f4": 0.5, "f5": 0.6, "f6": 0.7, "f7": 0.8
}

latencies = []

for _ in range(100):
    start = time.perf_counter()
    r = requests.post(URL, json=payload)

    end = time.perf_counter()

    latencies.append((end-start)*1000)

print("avg_ms:", statistics.mean(latencies))
print("p95_ms:", statistics.quantiles(latencies, n=20)[18])