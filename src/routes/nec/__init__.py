from flask import make_response, jsonify, request

from src.common import Logger
from src.core import Namespace
from src.routes.nec.schema import NecPriceVolumeDeliverableData

Client = Namespace("nec")
api = Client.api
log = Logger()


@api.route("/data", methods=["POST"])
def set_nec_pvd_data_singular():
    data = request.get_json()
    log.info("Request received : set_nec_pvd_data_singular")
    log.info(f"set_nec_pvd_data_singular : {data}")
    nec_model_schema = NecPriceVolumeDeliverableData()
    nec_model = nec_model_schema.dump(data)
    return make_response(jsonify(nec_model), 200)


@api.route("/parse_csv", methods=["POST"])
def set_nec_pvd_data_csv():
    log.info("Request received : set_nec_pvd_data_csv")
    return make_response({"ok": 1}, 200)
