import json
import math
import time
import sys
import os

from datetime import datetime
from typing import Union, List
from collections import deque
from elasticsearch import Elasticsearch, ConnectionError
from elasticsearch.helpers import BulkIndexError, parallel_bulk
from elasticsearch.exceptions import AuthorizationException, NotFoundError
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.errors import ServerSelectionTimeoutError


BULK_SIZE = 1000


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


def get_mongo_documents_count(client: MongoClient) -> int:
    try:
        document_db = client["docu_search"]
        collection = document_db["documents"]
        mongo_documents_count = collection.estimated_document_count()
        print(f"Number of documents to be inserted: {mongo_documents_count}")
        return mongo_documents_count
    except:
        print("Error! Failed to get documents from MongoDB.")


def get_mongo_documents(
    client: MongoClient, bulk_size: int = BULK_SIZE, skip: int = 0
) -> List[Cursor]:
    try:
        document_db = client["docu_search"]
        collection = document_db["documents"]
        mongo_documents = list(
            collection.find().sort("_id").limit(bulk_size).skip(skip)
        )
        print("Success! Retrieved documents from MongoDB.")
        return mongo_documents
    except:
        print("Error! Failed to get documents from MongoDB.")


def compute_batch_list(
    mongo_documents_count: int, bulk_size: int = BULK_SIZE
) -> List[int]:
    remaining_documents = mongo_documents_count
    batch_list = []

    print(f"Bulk size: {bulk_size}")

    number_of_batches = math.ceil(mongo_documents_count / bulk_size)
    print(f"Number of batches: {number_of_batches}")
    print()

    while remaining_documents > 0:
        number_of_batches -= 1
        remaining_documents -= bulk_size
        batch_number = number_of_batches * bulk_size
        batch_list.insert(0, batch_number)

    return batch_list


def get_es_client(config: dict) -> Elasticsearch:
    host = config["ES"]["HOST"]
    username = config["ES"]["USERNAME"]
    password = config["ES"]["PASSWORD"]
    elastic_client = Elasticsearch(
        host,
        http_auth=(username, password),
        scheme="https",
        http_compress=True,
        timeout=60,
        max_retries=100,
        retry_on_timeout=True,
    )
    try:
        # test connection to elasticsearch client
        elastic_client.nodes.info()
        print("Success! Connected to Elasticsearch.")
        return elastic_client
    except ConnectionError:
        print("Error! Failed to connect to Elasticsearch.")


def handle_nan_value(string: Union[str, float]) -> str:
    if type(string) == str:
        return string
    else:
        empty_string = ""
        return empty_string


def build_es_actions(mongo_documents: List[Cursor], next_index: str) -> List[dict]:
    es_actions = []
    for document in mongo_documents:
        content = handle_nan_value(document["content"])
        es_actions.append(
            {
                "_op_type": "create",
                "_index": next_index,
                "_type": "_doc",
                "_id": str(document["_id"]),
                "doc": {
                    "topic": document["topic"],
                    "content": content,
                },
            }
        )
    return es_actions


def bulk_create_es_documents(client: Elasticsearch, actions: List[dict]):
    max_number_of_attempts = 10
    for attempt in range(max_number_of_attempts):
        try:
            deque(
                parallel_bulk(client, actions, thread_count=8, chunk_size=BULK_SIZE),
                maxlen=0,
            )
            number_of_documents = len(actions)
            print(f"Success! Inserted {number_of_documents} ES documents.")
            print()

        except AuthorizationException:
            print("Request throttled due to too many requests. Retrying: ")
            print(f"Attempt {attempt+1} of {max_number_of_attempts}")
            time.sleep(30)

        except BulkIndexError as exception:
            print("Error! Failed to run bulk create on Elasticsearch.")
            errors = exception.errors
            errorIds = [d["create"]["_id"] for d in errors]
            print("IDs of failed documents: {}".format(errorIds))

        else:
            break


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def batch_process(config):
    mongo_client = get_mongo_client(config)
    es_client = get_es_client(config)
    print()

    es_indices_info = get_es_indices_info(es_client, config)
    next_index = es_indices_info["next_index"]
    past_index = es_indices_info["past_index"]

    # create next index
    try:
        es_client.indices.create(index=next_index)
        print(f"Success! Next index created: {next_index}.")
        print()
    except NotFoundError:
        print("Error! Failed to create new index.")
        sys.exit(1)

    mongo_documents_count = get_mongo_documents_count(mongo_client)
    batch_list = compute_batch_list(mongo_documents_count, BULK_SIZE)

    number_of_batches = len(batch_list)
    number_of_batches_remaining = number_of_batches

    for batch in batch_list:
        batch_number = batch_list.index(batch) + 1
        print(f"Batch {batch_number} of {number_of_batches}")
        number_of_batches_remaining -= 1

        mongo_documents = get_mongo_documents(mongo_client, BULK_SIZE, batch)
        actions = build_es_actions(mongo_documents, next_index)
        bulk_create_es_documents(es_client, actions)

    # clean up alias and leftover indices
    handle_production_alias(es_client, next_index, past_index, config)


def get_production_indices(
    list_of_indices: List[str], production_index_prefix: str
) -> List[str]:
    production_indices = []
    for index in list_of_indices:
        if index.lower().startswith(production_index_prefix.lower()):
            production_indices.append(index)
    production_indices.sort()
    return production_indices


def get_past_index(production_indices: List[str]) -> str:
    past_index = production_indices[len(production_indices) - 1]
    return past_index


def get_past_index_count(past_index: str, production_index_prefix: str) -> int:
    past_index_count = int(past_index.removeprefix(f"{production_index_prefix}"))
    return past_index_count


def get_es_indices_info(client: Elasticsearch, config: dict):
    production_index_prefix = config["ES"]["INDEX_PREFIX"]

    indices_dict = client.indices.get_alias()
    list_of_indices = [*indices_dict]

    production_indices = get_production_indices(
        list_of_indices, production_index_prefix
    )
    past_index = get_past_index(production_indices)
    past_index_count = get_past_index_count(past_index, production_index_prefix)

    next_index_count = past_index_count + 1
    next_index = f"{production_index_prefix}{next_index_count:0>2}"

    es_indices_info = {
        "past_index": past_index,
        "past_index_count": past_index_count,
        "next_index": next_index,
        "next_index_count": next_index_count,
    }

    return es_indices_info


def handle_production_alias(
    client: Elasticsearch, next_index: str, past_index: str, config: dict
):
    production_alias = config["ES"]["PRODUCTION_ALIAS"]
    production_index_prefix = config["ES"]["INDEX_PREFIX"]

    # add alias to next index
    try:
        client.indices.put_alias(index=next_index, name=production_alias)
        print(f"Success! Production alias added to next index: {next_index}.")
    except NotFoundError:
        print("Error! Failed to add alias to next index")

    # delete alias from past index
    try:
        client.indices.delete_alias(index=past_index, name=production_alias)
        print(f"Success! Production alias deleted from past index: {past_index}.")
        print()
    except NotFoundError:
        print("Error! Failed to delete alias from past index")

    # keep next index and past index, delete the rest
    new_indices_dict = client.indices.get_alias()
    new_list_of_indices = [*new_indices_dict]
    production_indices = get_production_indices(
        new_list_of_indices, production_index_prefix
    )
    if len(production_indices) > 2:
        print("Cleaning up unused indices...")
        production_indices.remove(next_index)
        production_indices.remove(past_index)
        list_of_indices_to_delete = production_indices
        for index in list_of_indices_to_delete:
            try:
                client.indices.delete(index)
                print(f"Success! Deleted unused index: {index}.")
            except NotFoundError:
                print(f"Error! Failed to delete index: {index}.")


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, "./config.json")
    config = read_json(config_path)

    start_time = datetime.now()

    print("Start.")
    print(f"Start time: {start_time}")
    print()

    # batch_process(config)

    end_time = datetime.now()
    total_run_time = end_time - start_time

    print()
    print(f"Total run time: {total_run_time}")
    print()
    print(f"End time: {end_time}")
    print("End.")
