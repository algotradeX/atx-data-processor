import pandas as pd

import src.repository.nse_repository as nse_repo
from src.common import Logger
from src.routes.nse import NsePriceVolumeDeliverableData
from src.routes.nse.transformer import get_nse_daily_data_model_from_nse_pvd_data

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
    df = pd.read_csv(_localCsvUrl)
    nse_pvd_schema = NsePriceVolumeDeliverableData()
    for index, row in df.iterrows():
        log.info(f"create_nse_data_from_csv : index {index}")
        nse_data = nse_pvd_schema.dump(
            {
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
            }
        )
        upsert_nse_data_from_nse_pvd_data(nse_data)
