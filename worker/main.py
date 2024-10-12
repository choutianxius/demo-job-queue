import logging
import redis
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


r = redis.Redis(host="redis", port=6379, db=0, password="default")

KEY_FOR_Q = "jobs"
POLL_INTERVAL = 1.0


while True:
    time.sleep(POLL_INTERVAL)
    job = r.lpop(KEY_FOR_Q)

    if job is None:
        continue

    # run job
    splitted = job.decode("utf-8").split("$")
    if len(splitted) != 2:
        continue

    analysis_type, timestamp = splitted

    if analysis_type != "shadow" and analysis_type != "thermal":
        continue

    logger.info("Running %s analysis for %s", analysis_type, timestamp)
    r.hset(job, "status", "running")

    # pretend that we are doing work
    time.sleep(30)

    r.hset(job, "result", "some result")
    r.hset(job, "status", "finished")
    logger.info("Finished %s analysis for %s", analysis_type, timestamp)
