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
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)

    def __repr__(self):
        return (
            "<NseDailyDataModel(timestamp='%s', open='%s', close='%s', high='%s', low='%s', volume='%s',"
            " symbol='%s', createdTime='%s', updatedTime='%s')>"
            % (
                self.timestamp,
                self.open,
                self.close,
                self.high,
                self.low,
                self.volume,
                self.symbol,
                self.created_time,
                self.updated_time,
            )
        )
