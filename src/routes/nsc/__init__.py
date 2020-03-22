from flask import make_response, jsonify, request

from src.common import Logger
from src.core import Namespace
from src.routes.nsc.schema import NscPriceVolumeDeliverableData
from src.services.nsc_service import create_nsc_data_from_nsc_pvd_data
from src.util import parse_request_using_schema

Client = Namespace("nsc")
api = Client.api
log = Logger()


@api.route("/data", methods=["POST"])
def set_nsc_pvd_data_singular():
    nsc_pvd_data = parse_request_using_schema(request, NscPriceVolumeDeliverableData())
    create_nsc_data_from_nsc_pvd_data(nsc_pvd_data)
    return make_response(jsonify(nsc_pvd_data), 200)


@api.route("/parse_csv", methods=["POST"])
def set_nsc_pvd_data_csv():
    log.info("Request received : set_nsc_pvd_data_csv")
    return make_response({"ok": 1}, 200)
