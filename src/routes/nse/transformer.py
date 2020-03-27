from src.model.nse_model import NseDailyDataModel


def get_nse_daily_data_model_from_nse_pvd_data(nse_pvd_data):
    _timestamp = nse_pvd_data["timestamp"]
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
    return nse_data
