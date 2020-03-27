from time import sleep

from pymongo.errors import ServerSelectionTimeoutError
from sqlalchemy import exc

from src.app import server
from src.common import Logger
from src.routes.job.service import create_batch_job
from src.util.job import add_job_meta

log = Logger()
postgres = server.get_postgres()


def ping_mongo():
    try:
        return True if (server.get_mongo_db().command("ping")["ok"] == 1.0) else False
    except ServerSelectionTimeoutError:
        return False
    except Exception as e:
        log.error(f"ping_mongo: exception occurred {e}")
        return False


def ping_postgres():
    session = postgres.get_session()
    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        session.execute("SELECT 1")
        pass
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        log.error(f"ping_postgres : error occurred : {err}")
        return False
    return True


def ping_redis():
    return server.get_redis().health()


def redis_ping_worker_queue(resp, sleep_delay=0):
    add_job_meta()
    sleep(5 + sleep_delay)
    log.info("redis_ping_worker_queue : Worker queue active : " + resp)
    return resp


def ping_work_queue():
    # testing job queues
    high_p_job = server.get_job_queue().enqueue_job(
        redis_ping_worker_queue, priority="high", args=("PONG high", 1)
    )
    medium_p_job = server.get_job_queue().enqueue_job(
        redis_ping_worker_queue, priority="medium", args=("PONG medium", 3)
    )
    low_p_job = server.get_job_queue().enqueue_job(
        redis_ping_worker_queue, priority="low", args=("PONG low", 6)
    )
    batch_job_id = create_batch_job("pinging", [high_p_job, medium_p_job, low_p_job])
    return batch_job_id
