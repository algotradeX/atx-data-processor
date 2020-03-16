from flask import Blueprint
from dynaconf import settings


class Namespace(object):
    def __init__(self, path=None):
        self.baseAPIUrl = settings.API.VERSION + settings.APP_NAME
        self.path = path
        self.api = Blueprint(path, __name__, url_prefix=self.baseAPIUrl + "/" + path)
