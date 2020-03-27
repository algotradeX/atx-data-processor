from rq import Queue

from src.common import Singleton
from src.constants import JOB_KWARGS_DEFAULT

default_job_kwargs = JOB_KWARGS_DEFAULT


class RedisJobQueues(metaclass=Singleton):
    """
        A singleton Worker Queue from Redis
    """

    def __init__(self, redis_conn):
        self.redis_conn = redis_conn
        self.high_priority_queue = Queue(
            "atx_dp_high_priority_job_queue",
            is_async=True,
            connection=redis_conn,
            default_timeout=30,
        )
        self.medium_priority_queue = Queue(
            "atx_dp_medium_priority_job_queue",
            is_async=True,
            connection=redis_conn,
            default_timeout=120,
        )
        self.low_priority_queue = Queue(
            "atx_dp_low_priority_job_queue",
            is_async=True,
            connection=redis_conn,
            default_timeout=1200,
        )
        self.passive_priority_queue = Queue(
            "atx_dp_passive_priority_job_queue", is_async=True, connection=redis_conn
        )

    def get_hpq(self):
        return self.high_priority_queue

    def get_mpq(self):
        return self.medium_priority_queue

    def get_lpq(self):
        return self.low_priority_queue

    def get_passive_q(self):
        return self.passive_priority_queue

    def get_queue_by_name(self, queue_name):
        if queue_name == "atx_dp_high_priority_job_queue":
            return self.get_hpq()
        if queue_name == "atx_dp_medium_priority_job_queue":
            return self.get_mpq()
        if queue_name == "atx_dp_low_priority_job_queue":
            return self.get_lpq()
        if queue_name == "atx_dp_passive_priority_job_queue":
            return self.get_passive_q()

    def enqueue_job(self, func, **job_kwargs):
        job = None
        priority = job_kwargs["priority"] if "priority" in job_kwargs else "medium"
        args = job_kwargs["args"] if "args" in job_kwargs else ()
        kwargs = (
            {**default_job_kwargs, **job_kwargs["kwargs"]}
            if "kwargs" in job_kwargs
            else {**default_job_kwargs}
        )
        if priority == "high":
            job = self.high_priority_queue.enqueue(func, *args, **kwargs)
        if priority == "medium":
            job = self.medium_priority_queue.enqueue(func, *args, **kwargs)
        if priority == "low":
            job = self.low_priority_queue.enqueue(func, *args, **kwargs)
        if priority == "passive":
            job = self.passive_priority_queue.enqueue(func, *args, **kwargs)
        return job
