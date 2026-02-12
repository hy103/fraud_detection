import time
import requests
import statistics
import httpx
import numpy as np
import asyncio

URL = "http://127.0.0.1:8000/score"

NUM_REQUESTS = 100
CONCURRENT = 10


async def send_request(client, i):

    payload = {
        "transaction_id": "ftx_{i}",
        "amount": float(np.random.rand() * 1000),
        "user_id": f"user_{i}",
        "feature_1": 0.2,
        "feature_2": 0.5,
        "feature_3": 0.8
    }

    start = time.perf_counter()
    r = await client.post(URL, json=payload)
    latency = (time.perf_counter() - start)*1000
    return latency

async def run_test():
    semaphore = asyncio.Semaphore(10)

    async with httpx.AsyncClient() as client:
        start = time.perf_counter()

        async def bounded_request(i):
            async with semaphore:
                return await send_request(client, i)

        tasks = [bounded_request(i) for i in range(NUM_REQUESTS)]
        latencies = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - start

    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)

    print("Requests:", NUM_REQUESTS)
    print("p50 ms:", round(p50, 2))
    print("p95 ms:", round(p95, 2))
    print("Throughput rps:", round(NUM_REQUESTS / total_time, 2))



if __name__ == "__main__":
    asyncio.run(run_test())