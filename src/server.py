from dynaconf import settings
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS

from src.common import Singleton, line_profiler, Logger, add_flask_profiler
from src.db import Postgres, RedisConnector, RedisJobQueues, MongoConnector

log = Logger()


class Server(metaclass=Singleton):
    def __init__(self):
        app = Flask(__name__)
        add_flask_profiler(app)
        with app.app_context():
            log.info(f"starting {settings.APP_NAME} server on {settings.API.SERVER}")
        CORS(app)
        self.app = app
        self.docs = FlaskApiSpec(app)
        self.lineProfiler = line_profiler()
        log.info(f"starting {settings.APP_NAME} mongo connector {settings.MONGO}")
        self.mongo = MongoConnector(settings.MONGO)
        log.info(f"starting {settings.APP_NAME} postgres connector {settings.POSTGRES}")
        self.postgres = Postgres(settings.POSTGRES)
        """
            When worker fork's the parent process, the db engine & connection pool is included in that.
            But, the db connections should not be shared across processes, so we tell the engine
            to dispose of all existing connections, which will cause new ones to be opened in the child
            processes as needed.
            More info:
            https://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing
        """
        with app.app_context():
            self.postgres.get_engine().dispose()
        log.info(f"starting {settings.APP_NAME} redis connector {settings.REDIS}")
        self.redis = RedisConnector(settings.REDIS)
        log.info(
            f"starting {settings.APP_NAME} rq dashboard at http://"
            f"{settings.API.SERVER.url}:{settings.API.SERVER.port}{settings.API.VERSION}{settings.APP_NAME}/rq"
        )
        app.config["RQ_DASHBOARD_REDIS_URL"] = settings.REDIS.url
        log.info(f"starting {settings.APP_NAME} redis job queues")
        self.redisJobQueues = RedisJobQueues(self.redis.get_redis_conn())
        log.info(f"starting {settings.APP_NAME} redis job queues")
        self.redisJobQueues = RedisJobQueues(self.redis.get_redis_conn())
        log.info(f"started {settings.APP_NAME} server on {settings.API.SERVER}")

    def get_app(self):
        return self.app

    def get_docs(self):
        return self.docs

    def get_line_profiler(self):
        return self.lineProfiler

    def get_mongo_db(self):
        return self.mongo.db

    def get_postgres(self):
        return self.postgres

    def get_redis(self):
        return self.redis

    def get_job_queue(self):
        return self.redisJobQueues
