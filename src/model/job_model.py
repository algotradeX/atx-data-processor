from marshmallow import Schema, fields


class BatchJob(Schema):
    _id = fields.Str(required=True)
    description = fields.Str(required=True)
    finished = fields.Bool(required=True)
    stats = fields.Raw(required=True)
    jobs = fields.Raw(required=True)
    createdTime = fields.Raw()
    updatedTime = fields.Raw()

    class Meta:
        strict = True
        dateformat = "iso"
