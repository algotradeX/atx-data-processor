import src.repository.nse_repository as nse_repo
from src.model.nse_model import NseDailyDataModel

from datetime import datetime


def create_nse_data_from_nse_pvd_data(nse_pvd_data):
    _timestamp = datetime.strptime(nse_pvd_data["date"], "%d-%b-%Y")
    _open = nse_pvd_data["open"]
    _close = nse_pvd_data["close"]
    _high = nse_pvd_data["high"]
    _low = nse_pvd_data["low"]
    _volume = nse_pvd_data["total_traded_qty"]
    _interval = 24 * 60
    _symbol = (
        nse_pvd_data["symbol"] + "_" + nse_pvd_data["series"] + "_" + str(_interval)
    )
    nse_data = NseDailyDataModel(
        timestamp=_timestamp,
        open=_open,
        close=_close,
        high=_high,
        low=_low,
        volume=_volume,
        symbol=_symbol,
    )
    nse_repo.create_one(nse_data)
