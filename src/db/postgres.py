from sqlalchemy import create_engine
from dynaconf import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.common import Singleton, Logger

log = Logger()


class Postgres(metaclass=Singleton):
    """
    A singleton Connector for Postgres
    """

    def __init__(self, pg_settings=settings["POSTGRES"]):
        # creates a create_engine instance at the bottom of the file
        engine = create_engine(
            pg_settings["uri"] + "/" + pg_settings["db"], pool_pre_ping=True
        )
        # constructs a base class for the declarative class definition and assigns it to the base variable
        base = declarative_base()
        # The last step in our configuration is to add Base.metadata.create_all(engine).
        # It will add the classes (we’ll write them in a bit) as new tables in the database we just created.
        base.metadata.create_all(engine)
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        base.metadata.bind = engine

        db_session = sessionmaker(bind=engine)
        # A db_session() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the database session object.
        session = db_session()

        self.engine = engine
        self.connection = self.engine.connect()
        self.base = base
        self.session = session
        log.info(f"Postgres Instance created")

    def get_engine(self):
        return self.engine

    def get_connection(self):
        return self.connection

    def get_base(self):
        return self.base

    def get_session(self):
        return self.session
