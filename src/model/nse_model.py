from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Float, TIMESTAMP, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class NseDailyDataModel(Base):
    """Model for NSE Daily Data"""

    __tablename__ = "nse_data_daily"

    timestamp: datetime
    open: float
    close: float
    high: float
    low: float
    volume: float
    symbol: str

    timestamp = Column(TIMESTAMP, primary_key=True)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    symbol = Column(VARCHAR(20))
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)
