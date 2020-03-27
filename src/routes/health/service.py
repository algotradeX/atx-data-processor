from sqlalchemy import exc

from src.app import server
from src.common import Logger

log = Logger()
postgres = server.get_postgres()


def ping_postgres():
    session = postgres.get_session()
    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        session.execute("SELECT 1")
        pass
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        log.error(f"ping_postgres : error occurred : {err}")
        return False
    return True


def ping_redis():
    return server.get_redis().health()
