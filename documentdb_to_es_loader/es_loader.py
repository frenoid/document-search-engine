import json

from elasticsearch import Elasticsearch, helpers, ConnectionError
from elasticsearch.helpers import BulkIndexError
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.errors import ServerSelectionTimeoutError


def get_mongo_client(config: dict) -> MongoClient:
    host = config["MONGO"]["HOST"]
    username = config["MONGO"]["USERNAME"]
    password = config["MONGO"]["PASSWORD"]
    db = config["MONGO"]["DB"]
    mongo_client = MongoClient(
        host,
        username=username,
        password=password,
        authSource=db,
    )
    try:
        # test connection to mongo client
        mongo_client.admin.command("ismaster")
        print("Success! Connected to MongoDB.")
        return mongo_client
    except ServerSelectionTimeoutError:
        print("Error! Failed to connect to MongoDB.")


def get_mongo_documents(client: MongoClient, bulk_size: int = 5) -> list[Cursor]:
    try:
        document_db = client["docu_search"]
        collection = document_db["documents"]
        mongo_documents = list(collection.find().sort("_id").limit(bulk_size))
        print("Success! Retrieved documents from MongoDB.")
        return mongo_documents
    except:
        print("Error! Failed to get documents from MongoDB.")


def get_es_client(config: dict) -> Elasticsearch:
    host = config["ES"]["HOST"]
    username = config["ES"]["USERNAME"]
    password = config["ES"]["PASSWORD"]
    elastic_client = Elasticsearch(
        host,
        http_auth=(username, password),
        scheme="https",
    )
    try:
        # test connection to elasticsearch client
        elastic_client.nodes.info()
        print("Success! Connected to Elasticsearch.")
        return elastic_client
    except ConnectionError:
        print("Error! Failed to connect to Elasticsearch.")


def build_es_actions(mongo_documents: list[Cursor], config: dict) -> list[dict]:
    index = config["ES"]["INDEX"]
    es_actions = []
    for document in mongo_documents:
        es_actions.append(
            {
                "_op_type": "create",
                "_index": index,
                "_type": "_doc",
                "_id": str(document["_id"]),
                "doc": {
                    "topic": document["topic"],
                    "content": document["content"],
                },
            }
        )
    return es_actions


def bulk_create_es_documents(client: Elasticsearch, actions: list[dict]):
    try:
        helpers.bulk(client, actions)
        print("Success! Created ES documents.")
    except BulkIndexError as exception:
        print("Error! Failed to run bulk create on Elasticsearch.")
        errors = exception.errors
        errorIds = [d["create"]["_id"] for d in errors]
        print("IDs of failed documents: {}".format(errorIds))


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    config = read_json("config.json")

    mongo_client = get_mongo_client(config)
    mongo_documents = get_mongo_documents(mongo_client)
    actions = build_es_actions(mongo_documents, config)

    es_client = get_es_client(config)
    bulk_create_es_documents(es_client, actions)

    print()
    print("End.")
