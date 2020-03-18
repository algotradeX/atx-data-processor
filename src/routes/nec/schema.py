from marshmallow import Schema, fields, post_load

"""
https://www1.nseindia.com/products/content/equities/equities/eq_security.htm
Model for Security-wise Price volume & Deliverable position data
:parameter : Symbol
:parameter : Series
"""


class NecPriceVolumeDeliverableData(Schema):
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

    @post_load
    def date_to_string(self, in_data, **kwargs):
        if "date" in in_data:
            in_data["timestamp"] = str(in_data["date"])

    class Meta:
        strict = True
        dateformat = "iso"
