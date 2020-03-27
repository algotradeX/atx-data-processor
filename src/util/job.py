import socket
from functools import reduce

from rq import get_current_job

from src.common import Logger

log = Logger()


def add_job_meta():
    job = get_current_job()
    ip = None
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        log.warning("add_job_meta : Exception while ip extraction " + str(e))
        ip = socket.gethostbyname("")
    job.meta["handler"] = ip
    job.save_meta()


def update_job_array_with_meta(job_array):
    job_array_with_meta = []
    for job in job_array:
        if hasattr(job, "meta"):
            if "handler" in job.meta:
                ip = job.meta["handler"]
            else:
                ip = None
        else:
            ip = None
        if job is not None:
            job_array_with_meta.append(
                {
                    "_id": job.id,
                    "status": job.get_status(),
                    "ip": ip,
                    "func": str(job.description),
                    "args": str(job.args),
                    "kwargs": str(job.kwargs),
                    "result": job.result,
                    "failure": job.exc_info,
                }
            )
        else:
            job_array_with_meta.append(
                {
                    "_id": None,
                    "status": "notfound",
                    "ip": ip,
                    "result": "Job not found in Redis",
                }
            )
    return job_array_with_meta


def is_batch_job_finished(job_array_with_meta):
    return reduce(
        lambda a, b: a and b["status"] in ["finished", "failed", "notfound"],
        job_array_with_meta,
        True,
    )


def batch_job_stats(job_array_with_meta):
    stats = {
        "queued": 0,
        "started": 0,
        "deferred": 0,
        "finished": 0,
        "failed": 0,
        "notfound": 0,
    }
    for job in job_array_with_meta:
        stats[job["status"]] += 1
    return stats
