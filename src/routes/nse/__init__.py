from flask import make_response, jsonify, request

from src.common import Logger
from src.core import Namespace
from src.routes.nse.schema import (
    NsePriceVolumeDeliverableData,
    NseDataCsvParseRequest,
    NseDataDeleteRequest,
    ProcessNseDataRequest,
)
from src.services.nse_service import (
    create_nse_data_from_nse_pvd_data,
    create_nse_data_from_csv,
    delete_nse_data,
    upsert_nse_data_from_nse_pvd_data,
    process_nse_data,
)
from src.util import parse_request_using_schema

Client = Namespace("nse")
api = Client.api
log = Logger()


@api.route("/data", methods=["POST"])
def set_nse_pvd_data_singular():
    nse_pvd_data = parse_request_using_schema(request, NsePriceVolumeDeliverableData())
    repo_resp = create_nse_data_from_nse_pvd_data(nse_pvd_data)
    return make_response(jsonify(repo_resp), 200)


@api.route("/data", methods=["PUT"])
def upsert_nse_pvd_data_singular():
    nse_pvd_data = parse_request_using_schema(request, NsePriceVolumeDeliverableData())
    repo_resp = upsert_nse_data_from_nse_pvd_data(nse_pvd_data)
    return make_response(jsonify(repo_resp), 200)


@api.route("/data", methods=["DELETE"])
def delete_nse_pvd_data_singular():
    nse_delete_data = parse_request_using_schema(request, NseDataDeleteRequest())
    repo_resp = delete_nse_data(nse_delete_data)
    return make_response(jsonify(repo_resp), repo_resp["status"])


@api.route("/parse_csv", methods=["POST"])
def set_nse_pvd_data_csv():
    nse_data_csv_req = parse_request_using_schema(request, NseDataCsvParseRequest())
    service_resp = create_nse_data_from_csv(nse_data_csv_req)
    return make_response(jsonify(service_resp), 200)


@api.route("/process", methods=["POST"])
def process_nse_pvd_data():
    process_nse_pvd_data_request = parse_request_using_schema(
        request, ProcessNseDataRequest()
    )
    service_resp = process_nse_data(process_nse_pvd_data_request)
    return make_response(jsonify(service_resp), service_resp["status"])
