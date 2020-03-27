from dynaconf import settings
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS

from src.common import Singleton, line_profiler, Logger, add_flask_profiler
from src.db import Postgres

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
        log.info(f"starting {settings.APP_NAME} postgres connector {settings.POSTGRES}")
        self.postgres = Postgres(settings.POSTGRES)
        log.info(f"started {settings.APP_NAME} server on {settings.API.SERVER}")

    def get_app(self):
        return self.app

    def get_docs(self):
        return self.docs

    def get_line_profiler(self):
        return self.lineProfiler

    def get_postgres(self):
        return self.postgres
