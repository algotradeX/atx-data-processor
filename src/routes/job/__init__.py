from src.common.logger import Logger
from src.core.namespace import Namespace
from src.services.job_service import (
    view_or_update_batch_job,
    clear_all_failed_jobs,
    clean_queue,
    requeue_all_failed_jobs,
    get_all_queue_stats,
    restart_batch_job,
    get_all_workers,
    kill_all_zombie_workers,
)

Job = Namespace("job")
api = Job.api
log = Logger()


# API to clear all failed job queue
@api.route("/all/failed/remove", methods=["GET"])
def remove_failed_jobs():
    log.info(f"Request received : clean_failed_jobs")
    response = clear_all_failed_jobs()
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to requeue all failed jobs in all queues
@api.route("/all/failed/requeue", methods=["GET"])
def requeue_failed_jobs():
    log.info(f"Request received : requeue_failed_jobs")
    response = requeue_all_failed_jobs()
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to view queue stats
@api.route("/queue/all/stats", methods=["GET"])
def view_all_q_stats():
    log.info(f"Request received : view_all_q_stats")
    response = get_all_queue_stats()
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to clean up job queue given queue name
@api.route("/queue/<queue_name>/clean", methods=["GET"])
def clean_queue_given_name(queue_name):
    log.info(f"Request received : clean_queue {queue_name}")
    response = clean_queue(queue_name)
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to view or update batch job status
@api.route("/batch/view/<batch_job_id>", methods=["GET"])
def view_or_update_job(batch_job_id):
    log.info(f"Request received : view_or_update_job with id {batch_job_id}")
    response = view_or_update_batch_job(batch_job_id)
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to requeue all unfinished jobs in a batch job
@api.route("/batch/restart/<batch_job_id>", methods=["GET"])
def reinitiate_batch_job(batch_job_id):
    log.info(f"Request received : restart_batch_job with id {batch_job_id}")
    response = restart_batch_job(batch_job_id)
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to view worker stats
@api.route("/worker/all", methods=["GET"])
def view_all_workers():
    log.info(f"Request received : view_all_workers")
    response = get_all_workers()
    return {"statusCode": 200 if response["success"] else 500, **response}


# API to kill zombie workers : workers that received interrupted shutdown but still logged in redis as workers
@api.route("/worker/killZombies", methods=["GET"])
def kill_zombie_workers():
    log.info(f"Request received : view_all_workers")
    response = kill_all_zombie_workers()
    return {"statusCode": 200 if response["success"] else 500, **response}
