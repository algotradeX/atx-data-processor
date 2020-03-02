from dynaconf import settings
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS

from src.common import Singleton


class Server(metaclass=Singleton):
    def __init__(self):
        app = Flask(__name__)
        CORS(app)
        self.app = app
        self.docs = FlaskApiSpec(app)
        print("started " + settings.SERVICE.NAME + " server on", settings.API.SERVER)

    def get_app(self):
        return self.app

    def get_docs(self):
        return self.docs

