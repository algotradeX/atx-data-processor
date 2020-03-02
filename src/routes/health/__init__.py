from flask import url_for

from src.app import app
from src.common import Logger
from src.core.namespace import Namespace
from src.util import has_no_empty_params

Client = Namespace("health")
api = Client.api
log = Logger()


@api.route("/ping", methods=["GET"])
def get_health():
    log.info("Request received : ping")
    if True:
        health = "OK"
    resp = {"health": health}
    return {"statusCode": 200, "data": resp}


@api.route("/sitemap")
def site_map():
    log.info("Request received : sitemap")
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return {"statusCode": 200, "sitemap": links}
