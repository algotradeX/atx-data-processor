import json
from dataclasses import asdict

from datetime import datetime, timedelta

from src.common import Logger
from src.services.nse_service import fetch_dataframe_between_dates

log = Logger()


def fetch_dashboard_graph_data(fetch_dashboard_data_req):
    log.info(f"get_dashboard_graph_data : req={fetch_dashboard_data_req}")
    symbol = fetch_dashboard_data_req["symbol"]
    series = fetch_dashboard_data_req["series"]
    interval = fetch_dashboard_data_req["interval"]
    date_string = fetch_dashboard_data_req["date"]
    page = fetch_dashboard_data_req["page"]
    ipp = fetch_dashboard_data_req["ipp"]
    start_date = datetime.strptime(date_string, "%d-%b-%Y %H:%M:%S")
    graph_plot_data = fetch_dataframe_between_dates(
        str(symbol) + "_" + str(series) + "_" + str(interval),
        start_date + timedelta(days=-page * ipp),
        start_date,
    )
    graph_plot_dict = {}
    for d in graph_plot_data:
        d_dict = asdict(d)
        key = d_dict["timestamp"].timestamp()
        graph_plot_dict[key] = d_dict
    graph_data = {"meta": {}, "events": {}, "data": graph_plot_dict}
    return {"data": graph_data, "success": True, "status": 200}
