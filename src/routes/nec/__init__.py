from flask import make_response, jsonify, request

from src.common import Logger
from src.core import Namespace
from src.routes.nec.schema import NecPriceVolumeDeliverableData
from src.util import parse_request_using_schema

Client = Namespace("nec")
api = Client.api
log = Logger()


@api.route("/data", methods=["POST"])
def set_nec_pvd_data_singular():
    nec_pvd_data = parse_request_using_schema(request, NecPriceVolumeDeliverableData())
    return make_response(jsonify(nec_pvd_data), 200)


@api.route("/parse_csv", methods=["POST"])
def set_nec_pvd_data_csv():
    log.info("Request received : set_nec_pvd_data_csv")
    return make_response({"ok": 1}, 200)
