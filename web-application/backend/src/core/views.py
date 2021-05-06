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

def upvote_document(topic: str, additional_upvotes: int) -> int:
    client = get_mongo_client() 
    db = client["docu_search"]

    return 1

def downvote_document(topic: str, additional_downvotes: int) -> int:
    client = get_mongo_client() 
    db = client["docu_search"]

    return 1

@csrf_exempt
def upvote_handler(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"status": "wrong method"}, 
            status=HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.body)
    print(data)

    new_upvote_count = upvote_document(topic="foo", additional_upvotes=int(data["additional_upvotes"]))
    
    return JsonResponse({"new_upvote_count": new_upvote_count})

@csrf_exempt
def downvote_handler(request) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"status": "wrong method"}, 
            status=HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.body)
    print(data)

    new_downvote_count = downvote_document(topic=data["topic"], additional_downvotes=int(data["additional_downvotes"]))

    return JsonResponse({"new_downvote_count": new_downvote_count})

@csrf_exempt
def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "OK"})


