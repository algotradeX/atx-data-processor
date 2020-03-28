import calendar
from datetime import datetime, timedelta

from rq import Worker
from rq.job import Job

from src.app import server
from src.common import Logger
from src.repository import job_repository
from src.util.job import (
    update_job_array_with_meta,
    add_job_meta,
    is_batch_job_finished,
    batch_job_stats,
)
from src.util.sequence import fetch_unique_uuid_md5_id

log = Logger()


def enqueue_job(foo, priority, args):
    job_id = server.get_job_queue().enqueue_job(foo, priority=priority, args=args)
    return job_id


def create_batch_job(desc, job_array):
    seq_id = fetch_unique_uuid_md5_id()
    log.info(f"create_batch_job : creating new batch job for {desc} with id {seq_id}")

    job_array_with_meta = update_job_array_with_meta(job_array)
    insert_resp = job_repository.create_one(
        {
            "_id": seq_id,
            "description": desc,
            "finished": is_batch_job_finished(job_array_with_meta),
            "stats": batch_job_stats(job_array_with_meta),
            "jobs": job_array_with_meta,
        }
    )
    if insert_resp.acknowledged:
        server.get_job_queue().enqueue_job(
            post_batch_job,
            priority="passive",
            args=(tuple([seq_id])),
            kwargs={"job_id": seq_id},
        )
        server.get_job_queue().enqueue_job(
            poll_batch_job, priority="low", args=(tuple([seq_id]))
        )
        return seq_id
    else:
        log.error(f"create_batch_job : failed to create new batch job with id {seq_id}")
        return None


def clear_all_failed_jobs():
    jq = server.get_job_queue()
    queues = [jq.get_hpq(), jq.get_mpq(), jq.get_lpq(), jq.get_passive_q()]
    for queue in queues:
        registry = queue.failed_job_registry
        registry.cleanup(
            calendar.timegm((datetime.utcnow() + timedelta(days=1)).utctimetuple())
        )
    return {"success": True}


def requeue_all_failed_jobs():
    jq = server.get_job_queue()
    queues = [jq.get_hpq(), jq.get_mpq(), jq.get_lpq(), jq.get_passive_q()]
    for queue in queues:
        failed_job_registry = queue.failed_job_registry
        for job_id in failed_job_registry.get_job_ids():
            failed_job_registry.requeue(job_id)
    return {"success": True}


def clean_queue(queue_name):
    queue = server.get_job_queue().get_queue_by_name(queue_name)
    queue.empty()
    return {"success": True}


def get_all_queue_stats():
    all_stats = {}
    jq = server.get_job_queue()
    queues = [jq.get_hpq(), jq.get_mpq(), jq.get_lpq(), jq.get_passive_q()]
    for queue in queues:
        all_stats.update({queue.name: len(queue.jobs)})
    return {"success": True, "body": all_stats}


def get_all_workers():
    worker_stats = {}
    workers = Worker.all(connection=server.get_redis().get_redis_conn())
    for worker in workers:
        worker_stats.update(
            {
                worker.name: {
                    "key": str(worker.key),
                    "name": str(worker.name),
                    "hostname": str(worker.hostname),
                    "pid": str(worker.pid),
                    "state": str(worker.state),
                    "birthDate": str(worker.birth_date),
                    "lastHeartbeat": str(worker.last_heartbeat),
                }
            }
        )
    return {"success": True, "body": worker_stats}


def kill_all_zombie_workers():
    workers = Worker.all(connection=server.get_redis().get_redis_conn())
    for worker in workers:
        if worker.state == "?":
            log.info(f"kill_all_zombie_workers : {worker.key} is found to be zombie")
            job = worker.get_current_job()
            if job is not None:
                job.ended_at = datetime.utcnow()
                worker.failed_queue.quarantine(
                    job, exc_info=("Dead worker", "Moving job to failed queue")
                )
            log.info(f"kill_all_zombie_workers : {worker.key} registering death")
            worker.register_death()
    return {"success": True}


def view_or_update_batch_job(batch_job_id):
    batch_job = job_repository.find_one(batch_job_id)
    if batch_job is None:
        return {
            "success": False,
            "statusCode": 400,
            "error": f"Batch job not found with id {batch_job_id}",
        }
    if batch_job["finished"]:
        return {"success": True, "body": batch_job}
    job_id_array = [job["_id"] for job in batch_job["jobs"]]
    job_array = Job.fetch_many(
        job_id_array, connection=server.get_redis().get_redis_conn()
    )

    job_array_with_meta = update_job_array_with_meta(job_array)
    job_finished = is_batch_job_finished(job_array_with_meta)
    if job_finished:
        server.get_job_queue().enqueue_job(
            post_batch_job,
            priority="low",
            args=(tuple([batch_job_id])),
            kwargs={"job_id": batch_job_id},
        )

    update_resp = job_repository.update_one(
        batch_job_id,
        {
            "finished": job_finished,
            "stats": batch_job_stats(job_array_with_meta),
            "jobs": job_array_with_meta,
        },
    )

    if update_resp.acknowledged:
        server.get_job_queue().enqueue_job(
            poll_batch_job, priority="low", args=(tuple([batch_job_id]))
        )
        updated_batch_job = job_repository.find_one(batch_job_id)
        return {"success": True, "body": updated_batch_job}
    else:
        log.error(
            f"view_or_update_batch_job : failed to update new batch job with id {batch_job_id}"
        )
        return {
            "success": False,
            "error": f"Batch job update failed with id {batch_job_id}",
        }


def poll_batch_job(batch_job_id):
    add_job_meta()
    log.info(f"poll_batch_job : Polling batch job {batch_job_id} status...")
    view_or_update_batch_job(batch_job_id)


def post_batch_job(batch_job_id):
    add_job_meta()
    log.info(f"post_batch_job : Running task post batch job {batch_job_id} completion")
    return True


def restart_batch_job(batch_job_id):
    batch_job = job_repository.find_one(batch_job_id)
    redis_conn = server.get_redis().get_redis_conn()
    if batch_job is None:
        return {
            "success": False,
            "statusCode": 400,
            "error": f"Batch job not found with id {batch_job_id}",
        }
    all_jobs = batch_job["jobs"]
    for job_meta in all_jobs:
        if job_meta["status"] != "finished":
            log.info(f"For batch job {batch_job_id}, requeue job {job_meta['_id']}")
            job = Job.fetch(job_meta["_id"], redis_conn)
            job.requeue()
    job_repository.update_one(batch_job_id, {"finished": False})
    server.get_job_queue().enqueue_job(
        poll_batch_job, priority="low", args=(tuple([batch_job_id]))
    )
    return {"success": True, "batch_job_id": batch_job_id}
