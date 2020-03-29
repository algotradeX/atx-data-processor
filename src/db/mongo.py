from dynaconf import settings
from pymongo import MongoClient

from src.common import Singleton, Logger

log = Logger()


class MongoConnector(metaclass=Singleton):
    """
    A singleton Connector from Mongo
    """

    def __init__(self, mongo_settings=settings["MONGO"]):
        self.link = mongo_settings["uri"]
        self.db_name = mongo_settings["db"]
        self.client = MongoClient(
            self.link, connect=False, maxPoolSize=mongo_settings["max_pool_size"]
        )
        self.db = self.client[self.db_name]

    def get_db(self):
        return self.db

    def get_collection(self, table_name):
        return self.db[table_name]

    def health(self):
        try:
            return self.db.ping()
        except Exception as e:
            log.error(f"MongoConnector health exception {e}")
            return False
