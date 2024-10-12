from datetime import datetime
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import redis


KEY_FOR_Q = "jobs"
MAX_NUM_JOBS = 5

r = redis.Redis(host="redis", port=6379, db=0, password="default")

fastapi_app = FastAPI()


class ServiceRequestBody(BaseModel):
    timestamp: str


@fastapi_app.post("/api/shadow-analysis")
async def request_shadow_analysis(body: ServiceRequestBody):
    try:
        t = datetime.strptime(body.timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(
            400, "Timestamp should be in the format YYYY-MM-DD HH-mm-ss"
        )

    jobs_in_queue = r.llen(KEY_FOR_Q)
    if jobs_in_queue >= MAX_NUM_JOBS:
        raise HTTPException(
            503,
            f"Number of jobs waiting in queue has reached the maximum of {MAX_NUM_JOBS}",
        )

    job_key = f"shadow${body.timestamp}"
    status = r.hgetall(job_key)

    if status is not None and len(status) > 0:
        return status

    r.rpush(KEY_FOR_Q, job_key)
    r.hset(job_key, "status", "waiting")
    status = r.hgetall(job_key)

    return status


@fastapi_app.post("/api/thermal-analysis")
async def request_thermal_analysis(body: ServiceRequestBody):
    try:
        t = datetime.strptime(body.timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(
            400, "Timestamp should be in the format YYYY-MM-DD HH-mm-ss"
        )

    jobs_in_queue = r.llen(KEY_FOR_Q)
    if jobs_in_queue >= MAX_NUM_JOBS:
        raise HTTPException(
            503,
            f"Number of jobs waiting in queue has reached the maximum of {MAX_NUM_JOBS}",
        )

    job_key = f"thermal${body.timestamp}"
    status = r.hgetall(job_key)

    if status is not None and len(status) > 0:
        return status

    r.rpush(KEY_FOR_Q, job_key)
    r.hset(job_key, "status", "waiting")
    status = r.hgetall(job_key)

    return status


@fastapi_app.get("/api/status")
async def check_job_status(analysis_type: str, timestamp: str):
    if not (analysis_type == "shadow" or analysis_type == "thermal"):
        raise HTTPException(
            400, 'Unsupported analysis type, should be "shadow" or "thermal"'
        )

    try:
        t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(
            400, "Timestamp should be in the format YYYY-MM-DD HH-mm-ss"
        )

    k = f"{analysis_type}${timestamp}"
    status = r.hgetall(k)

    if status is None or len(status) == 0:
        raise HTTPException(404, "Analysis request not found")

    return status
