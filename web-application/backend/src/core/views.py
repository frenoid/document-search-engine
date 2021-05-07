from http import HTTPStatus
import json
import os
import pymongo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

MONGO_HOST = os.environ.get("MONGO_HOST","localhost")
MONGO_USER = os.environ.get("MONGO_USER","elasticsearch")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD","elasticsearch")
MONGO_PORT = os.environ.get("MONGO_PORT","27017") 
MONGO_AUTH_SOURCE = os.environ.get("MONGO_AUTH_SOURCE","docu_search")



def get_mongo_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(MONGO_HOST,
                          username=MONGO_USER,
                          password=MONGO_PASSWORD,
                          authSource=MONGO_AUTH_SOURCE)


# Expected values for vote_counter_field are
# 1) upvote_count
# 2) downvote_count
def change_mongo_vote_count(topic: str, vote_counter_field: str, vote_delta: int) -> int:
    # Initiate the db cursor
    # Pull up the docu_search collection
    db = get_mongo_client()["docu_search"]

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

def change_elastic_search_vote_count(topic:str, vote_counter_field: str, vote_delta: int) -> int:
    # @Yijun you can change the method signature as you please
    # I just left the stub to make your life easier
    print(f"Handle vote count for {topic} in ElasticSearch")

    return 1

def upvote_document(topic: str, additional_upvotes: int) -> int:
    # Handle in ElasticSearch
    change_elastic_search_vote_count(topic=topic,
        vote_counter_field="upvotes",
        vote_delta=additional_upvotes)

    # Handle in MongoDB
    return change_mongo_vote_count(topic=topic,
        vote_counter_field="upvote_count",
        vote_delta=additional_upvotes)

def downvote_document(topic: str, additional_downvotes: int) -> int:
    # Handle in ElasticSearch
    change_elastic_search_vote_count(topic=topic,
        vote_counter_field="downvotes",
        vote_delta=additional_downvotes)

    # Handle in MongoDB
    return change_mongo_vote_count(topic=topic,
        vote_counter_field="downvote_count",
        vote_delta=additional_downvotes)

@csrf_exempt
def upvote_handler(request) -> JsonResponse:
    """
    Method POST
    JSON body
    {
        "topic": str,
        "additional_upvotes": int
    }
    """

    # Check method
    if request.method != "POST":
        return JsonResponse({"status": "wrong method"},
            status=HTTPStatus.METHOD_NOT_ALLOWED)

    # validate that required fields are present
    data: dict = json.loads(request.body)
    for field in ["topic", "additional_upvotes"]:
        if data.get(field) is None:
            return JsonResponse({"error": f"missing JSON field '{field}'"},
                status=HTTPStatus.BAD_REQUEST)

    # Increment the upvotes in
    # 1) Mongo
    # 2) ElasticSearch
    new_upvote_count = upvote_document(topic=data["topic"],
        additional_upvotes=int(data["additional_upvotes"]))
    
    return JsonResponse({"new_upvote_count": new_upvote_count})

@csrf_exempt
def downvote_handler(request) -> JsonResponse:
    """
    Method POST
    JSON body
    {
        "topic": str,
        "additional_downvotes": int
    }
    """

    # Check method
    if request.method != "POST":
        return JsonResponse({"status": "wrong method"},
            status=HTTPStatus.METHOD_NOT_ALLOWED)

    # validate that required fields are present
    data: dict = json.loads(request.body)
    for field in ["topic", "additional_downvotes"]:
        if data.get(field) is None:
            return JsonResponse({"error": f"missing JSON field '{field}'"},
                status=HTTPStatus.BAD_REQUEST)

    # Increment the upvotes in
    # 1) Mongo
    # 2) ElasticSearch
    new_downvote_count = downvote_document(topic=data["topic"],
        additional_downvotes=int(data["additional_downvotes"]))
    
    return JsonResponse({"new_downvote_count": new_downvote_count})

@csrf_exempt
def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "OK"})


