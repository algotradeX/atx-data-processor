from src.app import server
from src.model.nsc_model import NscDailyDataModel

postgres = server.get_postgres()
session = postgres.get_session()


def create_one(data):
    if isinstance(data, NscDailyDataModel):
        session.add(data)
        session.commit()
    else:
        raise RuntimeError("Model error")
