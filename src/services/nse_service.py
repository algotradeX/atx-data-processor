import pandas as pd

import src.repository.nse_repository as nse_repo
from src.common import Logger
from src.lib.technical_indicators import (
    moving_average,
    exponential_moving_average,
    momentum,
    bollinger_bands,
    rate_of_change,
)
from src.routes.nse import NsePriceVolumeDeliverableData
from src.routes.nse.transformer import get_nse_daily_data_model_from_nse_pvd_data
from src.services.job_service import enqueue_job, create_batch_job

log = Logger()


def create_nse_data_from_nse_pvd_data(nse_pvd_data):
    log.info(f"nse_service : create_nse_data_from_nse_pvd_data : {nse_pvd_data}")
    nse_data = get_nse_daily_data_model_from_nse_pvd_data(nse_pvd_data)
    return nse_repo.create_one(nse_data)


def upsert_nse_data_from_nse_pvd_data(nse_pvd_data):
    log.info(f"nse_service : upsert_nse_data_from_nse_pvd_data : {nse_pvd_data}")
    nse_data = get_nse_daily_data_model_from_nse_pvd_data(nse_pvd_data)
    return nse_repo.upsert_one(nse_data)


def delete_nse_data(delete_nse_data_resp):
    log.info(f"nse_service : delete_nse_data : {delete_nse_data_resp}")
    nse_data_id = delete_nse_data_resp["timestamp"]
    return nse_repo.delete_one(nse_data_id)


def create_nse_data_from_csv(nse_csv_req):
    log.info(f"nse_service : create_nse_data_from_csv : {nse_csv_req}")
    _localCsvUrl = nse_csv_req["localCsvUrl"]
    _useWorkers = nse_csv_req["useWorkers"]

    df = pd.read_csv(_localCsvUrl)
    if _useWorkers:
        job_array = []
        for index, row in df.iterrows():
            job_id = enqueue_job(parse_one_row_of_nse_data_csv, "medium", (index, row))
            job_array.append(job_id)
        batch_job_id = create_batch_job("parse_nse_csv", job_array)
        return {"success": True, "batch_job_id": batch_job_id}
    else:
        for index, row in df.iterrows():
            parse_one_row_of_nse_data_csv(index, row)
        return {"success": True}


def parse_one_row_of_nse_data_csv(index, row):
    log.info(f"create_nse_data_from_csv : index {index}")
    nse_pvd_schema = NsePriceVolumeDeliverableData()
    nse_data_dict = {
        "symbol": row["Symbol"],
        "series": row["Series"],
        "date": row["Date"],
        "prev_close": row["Prev Close"],
        "open": row["Open Price"],
        "high": row["High Price"],
        "low": row["Low Price"],
        "last": row["Last Price"],
        "close": row["Close Price"],
        "average": row["Average Price"],
        "total_traded_qty": row["Total Traded Quantity"],
        "turnover": row["Turnover"],
        "no_of_trades": row["No. of Trades"],
        "deliverable_qty": row["Deliverable Qty"],
        "percent_daily_qty_to_traded_qty": row["% Dly Qt to Traded Qty"],
        "is_valid_data": True,
    }

    # manual fixes on csv data
    if nse_data_dict["deliverable_qty"] == "-":
        nse_data_dict["deliverable_qty"] = 0
        nse_data_dict["is_valid_data"] = False
    if nse_data_dict["percent_daily_qty_to_traded_qty"] == "-":
        nse_data_dict["percent_daily_qty_to_traded_qty"] = 0
        nse_data_dict["is_valid_data"] = False

    nse_data = nse_pvd_schema.dump(nse_data_dict)
    return upsert_nse_data_from_nse_pvd_data(nse_data)


def process_nse_data(process_nse_pvd_data_request):
    symbol = process_nse_pvd_data_request["symbol"]
    df = nse_repo.find_dataframe_by_symbol(symbol)
    enqueue_job(process_and_insert_dataframe_in_database, "high", (df, symbol))
    return {"success": True, "status": 200}


def process_and_insert_dataframe_in_database(df, symbol):
    log.info(f"process_and_insert_dataframe_in_database : symbol={symbol}")
    df = moving_average(df, "close", 20)
    df = exponential_moving_average(df, "close", 20)
    df = momentum(df, "close", 20)
    df = bollinger_bands(df, "close", 20)
    df = rate_of_change(df, "close", 20)
    df = df.fillna(0)
    nse_repo.save_processed_dataframe(df, symbol)
    return {"success": True, "status": 200}
