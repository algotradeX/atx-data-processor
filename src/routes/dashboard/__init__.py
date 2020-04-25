from flask import request, make_response, jsonify

from src.common import Logger
from src.core import Namespace
from src.routes.dashboard.schema import FetchDashboardDataSchema
from src.services.dashboard_service import fetch_dashboard_graph_data
from src.util import parse_request_using_schema

Client = Namespace("dashboard")
api = Client.api
log = Logger()


@api.route("/fetchGraphData", methods=["GET"])
def get_dashboard_graph_data():
    fetch_dashboard_data_req = parse_request_using_schema(
        request, FetchDashboardDataSchema()
    )
    service_resp = fetch_dashboard_graph_data(fetch_dashboard_data_req)
    return make_response(jsonify(service_resp), 200)
