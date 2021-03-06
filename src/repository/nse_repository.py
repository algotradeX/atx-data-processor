import pandas as pd

from datetime import datetime

from src.app import server
from src.common import Logger
from src.model.nse_model import NseDailyDataModel
from src.repository.repository_response import generate_response

postgres = server.get_postgres()
engine = postgres.get_engine()
session = postgres.get_session()
log = Logger()


def create_one(data):
    if not isinstance(data, NseDailyDataModel):
        raise RuntimeError("Model error")

    data.created_time = datetime.utcnow()
    data.updated_time = datetime.utcnow()
    session.add(data)
    session.commit()
    log.info(f"nse_repository : create_one : data = {data}")
    return generate_response(200, "create", True, repr(data))


def find_within_dates(symbol, t1, t2):
    nse_data = (
        session.query(NseDailyDataModel)
        .filter(
            NseDailyDataModel.symbol == symbol,
            NseDailyDataModel.timestamp.between(t1, t2),
        )
        .all()
    )
    return nse_data


def upsert_one(data):
    if not isinstance(data, NseDailyDataModel):
        raise RuntimeError("Model error")

    nse_data = (
        session.query(NseDailyDataModel)
        .filter(
            NseDailyDataModel.timestamp == data.timestamp,
            NseDailyDataModel.symbol == data.symbol,
        )
        .first()
    )
    if nse_data is not None:
        update_params = {
            "timestamp": data.timestamp,
            "open": data.open,
            "close": data.close,
            "high": data.high,
            "low": data.low,
            "volume": data.volume,
            "symbol": data.symbol,
            "updated_time": datetime.utcnow(),
        }
        session.query(NseDailyDataModel).filter(
            NseDailyDataModel.timestamp == data.timestamp,
            NseDailyDataModel.symbol == data.symbol,
        ).update(update_params)
        session.commit()
        updated_nse_data = (
            session.query(NseDailyDataModel)
            .filter(
                NseDailyDataModel.timestamp == data.timestamp,
                NseDailyDataModel.symbol == data.symbol,
            )
            .first()
        )
        log.info(f"nse_repository : update_one : updated_nse_data = {updated_nse_data}")
        return generate_response(200, "update", True, repr(updated_nse_data))
    else:
        return create_one(data)


def delete_one(data_id):
    nse_data_to_be_deleted = session.query(NseDailyDataModel).get(data_id)
    if nse_data_to_be_deleted is not None:
        session.delete(nse_data_to_be_deleted)
        session.commit()
        log.info(
            f"nse_repository : delete_one : deleted_nse_data = {nse_data_to_be_deleted}"
        )
        return generate_response(200, "delete", True, repr(nse_data_to_be_deleted))
    else:
        return generate_response(200, "delete", False, None)


def find_dataframe_by_symbol(symbol):
    return pd.read_sql_query(
        "select * from nse_data_daily where nse_data_daily.symbol = %(symbol)s",
        params={"symbol": symbol},
        con=engine,
    )


def save_processed_dataframe(df, symbol):
    table_name = "nse_data_daily_processed_" + str(symbol)

    df.to_sql(table_name, con=engine, if_exists="replace", chunksize=1000)
