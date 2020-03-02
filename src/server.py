from dynaconf import settings
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS

from src.common import Singleton, line_profiler


class Server(metaclass=Singleton):
    def __init__(self):
        app = Flask(__name__)
        with app.app_context():
            print("starting " + settings.APP_NAME + " server on", settings.API.SERVER)
        CORS(app)
        self.app = app
        self.docs = FlaskApiSpec(app)
        self.lineProfiler = line_profiler()
        print("started " + settings.APP_NAME + " server on", settings.API.SERVER)

    def get_app(self):
        return self.app

    def get_docs(self):
        return self.docs

    def get_line_profiler(self):
        return self.lineProfiler
