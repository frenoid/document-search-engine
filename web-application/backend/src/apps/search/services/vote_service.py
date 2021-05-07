import os
import pymongo
from elasticsearch import Elasticsearch

MONGO_HOST = os.environ.get("MONGO_HOST","localhost")
MONGO_USER = os.environ.get("MONGO_USER","elasticsearch")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD","elasticsearch")
MONGO_PORT = os.environ.get("MONGO_PORT","27017") 
MONGO_AUTH_SOURCE = os.environ.get("MONGO_AUTH_SOURCE","docu_search")

ES_HOST = os.environ.get("ES_HOST")
ES_USERNAME = os.environ.get("ES_USERNAME")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
ES_PRODUCTION_ALIAS = os.environ.get("ES_PRODUCTION_ALIAS")

def get_mongo_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(MONGO_HOST,
                          username=MONGO_USER,
                          password=MONGO_PASSWORD,
                          authSource=MONGO_AUTH_SOURCE)

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

# Expected values for vote_counter_field are
# 1) upvote_count
# 2) downvote_count
def change_mongo_vote_count(topic: str, vote_counter_field: str, vote_delta: int) -> int:
    # Initiate the db cursor
    # Pull up the docu_search collection
    db = get_mongo_client()["docu_search"]

    print(f"Handle vote count for MongoDB document topic {topic}")
    print(f"Change {vote_counter_field} on topic {topic} by {vote_delta}")

    # retrive the document by topic name
    doc = db.documents.find_one({"topic": topic},
        {"topic": 1, vote_counter_field: 1})

    # Raise exception if the document cannot be found
    if doc is None:
        raise KeyError(f"{topic} not found in MongoDB")

    # If the document does not have upvote_count field -
    # then update it
    if doc.get(vote_counter_field) is None:
        db.documents.update({"topic": topic}, {"$set": {vote_counter_field: vote_delta}})
        print(f"{topic} now has {vote_delta} {vote_counter_field}")

        return vote_delta
    else:
        db.documents.update({"topic": topic}, {"$inc": {vote_counter_field: vote_delta}})
        print(f"{topic} now has {vote_delta + doc.get(vote_counter_field)} {vote_counter_field}")

        return vote_delta + doc.get(vote_counter_field)

def change_elastic_search_vote_count(id: str, vote_counter_field: str, vote_delta: int = 1) -> int:
    print(f"Handle vote count for Elasticsearch doc {id}")
    print(f"Change {vote_counter_field} on id {id} by {vote_delta}")

    index = ES_PRODUCTION_ALIAS
    es_client = get_es_client()

    # Search for elasticsearch doc by id
    try:
        get_document_query_body = {
            "query": {
                "term": {
                    "_id": id,
                }
            }
        }
        es_response = es_client.search(index=index, body=get_document_query_body, size=10)
        print(f"Success! Got search results for doc {id}.")
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

        # vote_counter_field field exists - increment vote_delta
        if vote_counter_field in doc:
            vote_delta = doc[vote_counter_field] + 1

        # Update vote_counter_field in elasticsearch
        try:
            update_document_query_body = {
                "doc": {
                    "doc": {
                        vote_counter_field: vote_delta
                    }
                }
            }
            es_response = es_client.update(index=index, id=id, body=update_document_query_body)
            print(f"Doc {id} now has {vote_delta} {vote_counter_field}")
        except Exception as e:
            print(f"Elasticsearch Error! {e}")
            return e


    return 1

def upvote_document(topic: str, additional_upvotes: int, id: str) -> int:
    # Handle in ElasticSearch
    change_elastic_search_vote_count(
        id=id,
        vote_counter_field="upvotes")

    # Handle in MongoDB
    return change_mongo_vote_count(topic=topic,
        vote_counter_field="upvote_count",
        vote_delta=additional_upvotes)

def downvote_document(topic: str, additional_downvotes: int, id: str) -> int:
    # Handle in ElasticSearch
    change_elastic_search_vote_count(
        id=id,
        vote_counter_field="downvotes")

    # Handle in MongoDB
    return change_mongo_vote_count(topic=topic,
        vote_counter_field="downvote_count",
        vote_delta=additional_downvotes)
