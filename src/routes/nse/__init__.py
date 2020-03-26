from flask import make_response, jsonify, request

from src.common import Logger
from src.core import Namespace
from src.routes.nse.schema import NsePriceVolumeDeliverableData
from src.services.nse_service import create_nse_data_from_nse_pvd_data
from src.util import parse_request_using_schema

Client = Namespace("nse")
api = Client.api
log = Logger()


@api.route("/data", methods=["POST"])
def set_nse_pvd_data_singular():
    nse_pvd_data = parse_request_using_schema(request, NsePriceVolumeDeliverableData())
    create_nse_data_from_nse_pvd_data(nse_pvd_data)
    return make_response(jsonify(nse_pvd_data), 200)


@api.route("/parse_csv", methods=["POST"])
def set_nse_pvd_data_csv():
    log.info("Request received : set_nse_pvd_data_csv")
    return make_response({"ok": 1}, 200)
