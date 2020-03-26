from src.app import server
from src.model.nse_model import NseDailyDataModel

postgres = server.get_postgres()
session = postgres.get_session()


def create_one(data):
    if isinstance(data, NseDailyDataModel):
        session.add(data)
        session.commit()
    else:
        raise RuntimeError("Model error")
