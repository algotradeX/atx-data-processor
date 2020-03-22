import src.repository.nsc_repository as nsc_repo
from src.model.nsc_model import NscDailyDataModel

from datetime import datetime


def create_nsc_data_from_nsc_pvd_data(nsc_pvd_data):
    _timestamp = datetime.strptime(nsc_pvd_data["date"], "%d-%b-%Y")
    _open = nsc_pvd_data["open"]
    _close = nsc_pvd_data["close"]
    _high = nsc_pvd_data["high"]
    _low = nsc_pvd_data["low"]
    _volume = nsc_pvd_data["total_traded_qty"]
    _interval = 24 * 60
    _symbol = (
        nsc_pvd_data["symbol"] + "_" + nsc_pvd_data["series"] + "_" + str(_interval)
    )
    nsc_data = NscDailyDataModel(
        timestamp=_timestamp,
        open=_open,
        close=_close,
        high=_high,
        low=_low,
        volume=_volume,
        symbol=_symbol,
    )
    nsc_repo.create_one(nsc_data)
