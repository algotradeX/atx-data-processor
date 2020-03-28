from marshmallow import Schema, fields, post_dump

from src.util import date_to_string_in_schema

"""
https://www1.nseindia.com/products/content/equities/equities/eq_security.htm
Model for Security-wise Price volume & Deliverable position data
:parameter : Symbol
:parameter : Series
"""


class NsePriceVolumeDeliverableData(Schema):
    symbol = fields.Str(required=True)
    series = fields.Str(required=True)
    date = fields.Str(required=True)
    timestamp = fields.DateTime()
    prev_close = fields.Float(required=True)
    open = fields.Float(required=True)
    high = fields.Float(required=True)
    low = fields.Float(required=True)
    close = fields.Float(required=True)
    last = fields.Float(required=True)
    average = fields.Float(required=True)
    total_traded_qty = fields.Int(required=True)
    turnover = fields.Float(required=True)
    no_of_trades = fields.Int(required=True)
    deliverable_qty = fields.Int(required=True)
    percent_daily_qty_to_traded_qty = fields.Float(required=True)
    is_valid_data = fields.Bool(missing=True)

    @post_dump
    def date_to_string(self, output, **kwargs):
        return date_to_string_in_schema(output)

    class Meta:
        strict = True
        dateformat = "iso"


class NseDataDeleteRequest(Schema):
    date = fields.Str(required=True)
    timestamp = fields.DateTime()

    @post_dump
    def date_to_string(self, output, **kwargs):
        return date_to_string_in_schema(output)

    class Meta:
        strict = True
        dateformat = "iso"


class NseDataCsvParseRequest(Schema):
    localCsvUrl = fields.Str(required=True)
    useWorkers = fields.Bool(missing=False)

    class Meta:
        strict = True
