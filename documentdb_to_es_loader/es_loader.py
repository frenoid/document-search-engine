import pymongo
import elasticsearch

import json


def get_mongo_client(config: dict) -> pymongo.MongoClient:
    host = config["MONGODB"]["HOST"]
    username = config["MONGODB"]["USERNAME"]
    password = config["MONGODB"]["PASSWORD"]
    return pymongo.MongoClient(
        host,
        username=username,
        password=password,
    )


def get_document(client: pymongo.MongoClient) -> str:
    document_db = client["docu_search"]
    collection = document_db["documents"]
    # document = collection.find_one()
    # return document
    return collection.full_name


def get_es_client(config: dict) -> elasticsearch.Elasticsearch:
    host = config["ES"]["HOST"]
    username = config["ES"]["USERNAME"]
    password = config["ES"]["PASSWORD"]

    return elasticsearch.Elasticsearch(
        host,
        http_auth=(username, password),
        scheme="https",
    )


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    config = read_json("config.json")

    mongo_client = get_mongo_client(config)
    one_document = get_document(mongo_client)
    print(one_document)

    es_client = get_es_client(config)
    print(es_client.indices.exists("doc-search-01"))
