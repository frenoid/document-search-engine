from __future__ import annotations

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


def search_documents(search_string: str, weights: dict = {}) -> Dict:
    es_client = get_es_client()

    index = ES_PRODUCTION_ALIAS
    fields_weight = build_query_with_weight(weights)
    body = {
        "query": {
            "query_string": {
                "query": search_string,
                "fields": fields_weight,
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

def build_query_with_weight(weights: dict) -> list[str]:
    # return with a list of str with format {field name}^{weight}
    #default
    if not weights:
        fields = ["doc.content", "doc.topic"]
        return fields
    else:
        fields = []
        for field, weight in weights.items():
            if weight > 1:
                fields.append(f"{field}^{weight}")
            else:
                fields.append(f"{field}")
        return fields
