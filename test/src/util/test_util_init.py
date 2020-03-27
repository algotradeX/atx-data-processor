from datetime import datetime
from unittest import TestCase

from marshmallow import Schema, fields, post_dump, ValidationError

from src.util import (
    get_initial_create_time_dict,
    get_update_time_dict,
    parse_request_using_schema,
    date_to_string_in_schema,
)


def mock_request(**kwargs):
    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def get_json(self):
            return self.json_data

    if kwargs["type"] == "valid":
        return MockResponse({"x": "value1", "date": "25-Feb-2019"})
    elif kwargs["type"] == "invalid":
        return MockResponse({"date": "25-Feb-2019"})

    return MockResponse(None)


class TestUtilInit(TestCase):
    def test_get_initial_create_time_dict(self):
        x = get_initial_create_time_dict()
        self.assertTrue("createdTime" in x)
        self.assertTrue(isinstance(x["createdTime"], datetime))
        self.assertTrue("updatedTime" in x)
        self.assertTrue(isinstance(x["updatedTime"], datetime))

    def test_get_update_time_dict(self):
        x = get_update_time_dict()
        self.assertTrue("updatedTime" in x)
        self.assertTrue(isinstance(x["updatedTime"], datetime))

    def test_parse_request_using_schema(self):
        class TestSchema(Schema):
            x = fields.Str(required=True)
            date = fields.Str(required=True)
            timestamp = fields.DateTime()

            @post_dump
            def date_to_string(self, output, **kwargs):
                return date_to_string_in_schema(output)

            class Meta:
                strict = True

        t_schema = TestSchema()
        valid_resp = mock_request(type="valid")
        data = parse_request_using_schema(valid_resp, t_schema)
        self.assertIsNotNone(data)
        self.assertIsNotNone(data["timestamp"])
        self.assertTrue(isinstance(data["timestamp"], datetime))

        invalid_resp = mock_request(type="invalid")
        with self.assertRaises(Exception) as context:
            parse_request_using_schema(invalid_resp, t_schema)

        self.assertTrue(isinstance(context.exception, ValidationError))
        self.assertTrue(len(context.exception.messages) == 1)
