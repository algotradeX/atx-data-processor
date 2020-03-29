from sqlalchemy import Column, Float, TIMESTAMP, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

from src.model.nse_model import NseDailyDataModel

Base = declarative_base()


class NseDailyDataProcessedModel(NseDailyDataModel):
    """Model for Processed NSE Daily Data"""

    __tablename__ = "nse_data_daily_processed"

    ma = Column(Float)

    def __repr__(self):
        return (
            "<NseDailyDataProcessedModel(timestamp='%s', open='%s', close='%s', high='%s', low='%s', volume='%s',"
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
