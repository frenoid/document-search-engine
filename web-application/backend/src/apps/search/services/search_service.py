import os
from typing import Dict
from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch, ConnectionError


load_dotenv(find_dotenv())

ES_HOST = os.environ.get("ES_HOST")
ES_USERNAME = os.environ.get("ES_USERNAME")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
ES_PRODUCTION_ALIAS = os.environ.get("ES_PRODUCTION_ALIAS")


def get_es_client() -> Elasticsearch:
    host = ES_HOST
    username = ES_USERNAME
    password = ES_PASSWORD
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


def search_documents(search_string: str) -> Dict:
    client = get_es_client()

    index = ES_PRODUCTION_ALIAS
    body = {
        "query": {
            "query_string": {
                "query": search_string,
                "fields": ["doc.content", "doc.topic"],
            }
        }
    }

    try:
        response = client.search(index=index, body=body, size=10)
        print("Success! Got search results.")
    except Exception as e:
        print(f"Error! {e}")
        return e

    topic_list = []
    hits = response["hits"]["hits"]

    for hit in hits:
        topic = hit["_source"]["doc"]["topic"]
        id = hit["_id"]
        hit_object = {"topic": topic, "id": id}
        topic_list.append(hit_object)

    response_object = {"response": topic_list}

    return response_object
