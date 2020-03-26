from sqlalchemy import Column, Float, TIMESTAMP, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NseDailyDataModel(Base):
    """Model for NSE Daily Data"""

    __tablename__ = "nse_data_daily"

    timestamp = Column(TIMESTAMP, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    symbol = Column(VARCHAR(20))

    def __repr__(self):
        return "NseModel"
