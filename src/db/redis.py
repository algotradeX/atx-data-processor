from redis import Redis, ConnectionPool
from dynaconf import settings

from src.common import Logger
from src.common import Singleton

log = Logger()


class RedisConnector(metaclass=Singleton):
    """
    A singleton Connector from Redis
    """

    def __init__(self, redis_setting=settings["REDIS"]):
        self.link = redis_setting["url"]
        self.redis_pool = ConnectionPool().from_url(self.link)
        self.redis_connection = Redis(connection_pool=self.redis_pool)

    def get_redis_conn(self):
        return self.redis_connection

    def get(self, key):
        return self.redis_connection.get(key)

    def set(self, key, value, expire_in_secs=None):
        return self.redis_connection.set(key, value, ex=expire_in_secs)

    def delete(self, key):
        return self.redis_connection.delete(key)

    def health(self):
        try:
            return self.ping()
        except Exception as e:
            log.error(f"RedisConnector health exception {e}")
            return False

    def ping(self):
        return self.redis_connection.ping()

    def info(self):
        return self.redis_connection.info()

    def scan_iter(self, key_namespace):
        return list(self.redis_connection.scan_iter(key_namespace))

    def getset(self, name, value):
        return self.redis_connection.getset(name, value)

    def incr(self, key, amt=1):
        return self.redis_connection.incr(key, amt)

    def expire(self, key, expire_in_secs):
        return self.redis_connection.expire(key, expire_in_secs)
