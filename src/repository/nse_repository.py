from datetime import datetime

from src.app import server
from src.common import Logger
from src.model.nse_model import NseDailyDataModel
from src.repository.repository_response import (
    delete_response,
    create_response,
    update_response,
)

postgres = server.get_postgres()
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
    return create_response(200, True, repr(data))


def upsert_one(data):
    if not isinstance(data, NseDailyDataModel):
        raise RuntimeError("Model error")

    nse_data = session.query(NseDailyDataModel).get(data.timestamp)
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
            NseDailyDataModel.timestamp == data.timestamp
        ).update(update_params)
        session.commit()
        updated_nse_data = session.query(NseDailyDataModel).get(data.timestamp)
        log.info(f"nse_repository : update_one : updated_nse_data = {updated_nse_data}")
        return update_response(200, True, repr(updated_nse_data))
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
        return delete_response(200, True, repr(nse_data_to_be_deleted))
    else:
        return delete_response(200, False, None)
