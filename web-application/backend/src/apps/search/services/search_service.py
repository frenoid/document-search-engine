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
    return elastic_client


def build_response_object(es_response: Dict) -> Dict:
    topic_list = []
    hits = es_response["hits"]["hits"]

    for hit in hits:
        topic = hit["_source"]["doc"]["topic"]
        id = hit["_id"]
        score = hit["_score"]
        hit_object = {"id": id, "topic": topic, "score": score}
        topic_list.append(hit_object)

    response_object = {"response": topic_list}

    return response_object


def search_documents(search_string: str) -> Dict:
    es_client = get_es_client()

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
        es_response = es_client.search(index=index, body=body, size=10)
        print("Success! Got search results.")
    except Exception as e:
        print(f"Elasticsearch Error! {e}")
        return e

    response_object = build_response_object(es_response)

    return response_object


def search_document_by_key(id: str) -> Dict:
    es_client = get_es_client()

    index = ES_PRODUCTION_ALIAS
    body = {
        "query": {
            "term": {
                "_id": id,
            }
        }
    }

    try:
        es_response = es_client.search(index=index, body=body, size=10)
        print("Success! Got search results.")
    except Exception as e:
        print(f"Elasticsearch Error! {e}")
        return e

    hits = es_response["hits"]["hits"]

    # Raise exception if the document cannot be found
    if len(hits) <= 0:
        raise KeyError(f"Doc {id} not found in Elasticsearch")
    # Raise exception duplicate documents found
    elif len(hits) != 1:
        raise KeyError(f"Duplicate docs with {id} found in Elasticsearch")
    # Exactly one document found
    else:
        doc: dict = hits[0]["_source"]["doc"]

    response_object = {"response": doc}

    return response_object
