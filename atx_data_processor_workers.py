import multiprocessing as mpu
import sys
import uuid
import socket

from rq import Worker, Connection

from src.common.logger import Logger
from src.app import server

log = Logger()
redis_conn = server.get_redis().get_redis_conn()


def get_ip_and_host():
    ip = "0.0.0.0"
    host = ""
    try:
        host = socket.gethostname()
        ip = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        log.info(f"get_ip_and_host : Exception occurred {e}")
        ip = socket.gethostbyname("")
    return ip + "_" + host


def start_worker(process_count):
    log.info(f"starting worker {process_count}")
    with Connection(redis_conn):
        if process_count % 4 == 0:
            w = Worker(
                ["atx_dp_high_priority_job_queue", "atx_dp_low_priority_job_queue"],
                connection=redis_conn,
                name="atx_dp_worker"
                + str(process_count)
                + "_"
                + str(get_ip_and_host())
                + "_"
                + str(uuid.uuid4()),
            )
            w.work()
        if process_count % 4 == 3:
            w = Worker(
                ["atx_dp_medium_priority_job_queue", "atx_dp_low_priority_job_queue"],
                connection=redis_conn,
                name="atx_dp_worker"
                + str(process_count)
                + "_"
                + str(get_ip_and_host())
                + "_"
                + str(uuid.uuid4()),
            )
            w.work()
        if process_count % 4 == 2:
            w = Worker(
                ["atx_dp_high_priority_job_queue", "atx_dp_medium_priority_job_queue"],
                connection=redis_conn,
                name="atx_dp_worker"
                + str(process_count)
                + "_"
                + str(get_ip_and_host())
                + "_"
                + str(uuid.uuid4()),
            )
            w.work()
        if process_count % 4 == 1:
            w = Worker(
                [
                    "atx_dp_high_priority_job_queue",
                    "atx_dp_medium_priority_job_queue",
                    "atx_dp_low_priority_job_queue",
                ],
                connection=redis_conn,
                name="atx_dp_worker"
                + str(process_count)
                + "_"
                + str(get_ip_and_host())
                + "_"
                + str(uuid.uuid4()),
            )
            w.work()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        worker_id = sys.argv[1]
        log.info(f"server core count: {mpu.cpu_count()}; worker id:{worker_id}")
        pool = mpu.Pool(processes=mpu.cpu_count())
        pool.map(
            start_worker, tuple(list(range(int(worker_id), mpu.cpu_count() * 4, 4)))
        )
    else:
        log.info(f"server core count: {mpu.cpu_count()}")
        pool = mpu.Pool(processes=mpu.cpu_count())
        pool.map(start_worker, tuple(list(range(1, mpu.cpu_count() + 1))))
