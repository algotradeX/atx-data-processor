from marshmallow import Schema, fields


class FetchDashboardDataSchema(Schema):
    symbol = fields.Str(required=True)
    series = fields.Str(required=True)
    interval = fields.Int(required=True)
    date = fields.Str(required=True)
    page = fields.Int(default=1)
    ipp = fields.Int(default=50)
    indicators = fields.List(fields.Str(), default=[])

    class Meta:
        strict = True
        dateformat = "iso"
