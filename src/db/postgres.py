from sqlalchemy import create_engine
from dynaconf import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

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

        # The sessionmaker function returns an object for building the particular session you want.
        # To understand the options passed to sessionmaker you need to know some terminology:
        # flushing is the process of updating the database with the objects you have been working with,
        # committing is the process of sending a COMMIT statement to the database to make those flushes permanent.
        db_sm = orm.sessionmaker(
            bind=engine, autoflush=True, autocommit=False, expire_on_commit=True
        )
        # bind=engine: this binds the session to the engine, the session will automatically create the connections it needs.
        #
        # autoflush=True: if you commit your changes to the database before they have been flushed, this option tells
        # SQLAlchemy to flush them before the commit is gone.
        #
        # autocommit=False: this tells SQLAlchemy to wrap all changes between commits in a transaction.
        # If autocommit=True is specified, SQLAlchemy automatically commits any changes after each flush; this is undesired in most cases.
        #
        # expire_on_commit=True: this means that all instances attached to the session will be fully expired after each
        # commit so that all attribute/object access subsequent to a completed transaction will load from the most recent database state.

        # The scoped_session() object ensures that a different session is used for each thread so that every request
        # can have its own access to the database.
        session = orm.scoped_session(db_sm)

        self.engine = engine
        self.base = base
        self.session = session
        log.info(f"Postgres Instance created")

    def get_engine(self):
        return self.engine

    def get_base(self):
        return self.base

    def get_session(self):
        return self.session
