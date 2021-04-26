import unittest

from bson import ObjectId
from documentdb_to_es_loader.es_loader import build_es_actions, handle_nan_value


class TestEsLoader(unittest.TestCase):
    def test_build_es_actions(self):

        # GIVEN
        config = {"ES": {"INDEX": "index"}}
        mongo_documents = [
            {
                "_id": ObjectId("0123456789ab0123456789ab"),
                "topic": "some topic 001",
                "content": "some content 001",
            },
            {
                "_id": ObjectId("0123456789ab0123456789ac"),
                "topic": "some topic 002",
                "content": "some content 002",
            },
            {
                "_id": ObjectId("0123456789ab0123456789ad"),
                "topic": "some topic 003",
                "content": "some content 003",
            },
            {
                "_id": ObjectId("0123456789ab0123456789ae"),
                "topic": "some topic 004",
                "content": float("NaN"),
            },
        ]

        # WHEN
        es_actions = build_es_actions(mongo_documents, config)

        # THEN
        expected_actions = [
            {
                "_op_type": "create",
                "_index": "index",
                "_type": "_doc",
                "_id": "0123456789ab0123456789ab",
                "doc": {
                    "topic": "some topic 001",
                    "content": "some content 001",
                },
            },
            {
                "_op_type": "create",
                "_index": "index",
                "_type": "_doc",
                "_id": "0123456789ab0123456789ac",
                "doc": {
                    "topic": "some topic 002",
                    "content": "some content 002",
                },
            },
            {
                "_op_type": "create",
                "_index": "index",
                "_type": "_doc",
                "_id": "0123456789ab0123456789ad",
                "doc": {
                    "topic": "some topic 003",
                    "content": "some content 003",
                },
            },
            {
                "_op_type": "create",
                "_index": "index",
                "_type": "_doc",
                "_id": "0123456789ab0123456789ae",
                "doc": {
                    "topic": "some topic 004",
                    "content": "",
                },
            },
        ]
        self.assertEqual(es_actions, expected_actions)

    def test_handle_nan_value(self):

        # GIVEN
        content_with_valid_string = "blah blah blah"
        content_with_nan_value = float("NaN")

        # WHEN
        content_with_valid_string_response = handle_nan_value(content_with_valid_string)
        content_with_nan_value_response = handle_nan_value(content_with_nan_value)

        # THEN
        empty_string = ""
        self.assertEqual(content_with_valid_string_response, content_with_valid_string)
        self.assertEqual(content_with_nan_value_response, empty_string)


if __name__ == "__main__":
    unittest.main()
