import unittest

from bson import ObjectId
from documentdb_to_es_loader.es_loader import build_es_actions


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
        ]
        self.assertEqual(es_actions, expected_actions)


if __name__ == "__main__":
    unittest.main()
