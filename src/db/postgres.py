import sqlalchemy as alchemist
from dynaconf import settings

from src.common import Singleton


class Postgres(metaclass=Singleton):
    """
    A singleton Connector for Postgres
    """

    def __init__(self, pg_settings=settings["POSTGRES"]):
        self.engine = alchemist.create_engine(
            pg_settings["uri"] + "/" + pg_settings["db"], pool_pre_ping=True
        )
        self.connection = self.engine.connect()
        print("Postgres Instance created")

    def get_engine(self):
        return self.engine

    def get_connection(self):
        return self.connection
