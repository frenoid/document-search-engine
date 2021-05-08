from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_GET, require_POST
from .services.search_service import search_documents, search_document_by_key
from .services.vote_service import upvote_document, downvote_document
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
import json
# Create your views here.

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_GET
def search(request):
    search_string = request.GET.get("search")

    if search_string:
        try:
            response = search_documents(search_string)
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({ "error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({ "error": "Search criteria cannot be null"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_GET
def retrieve_file_details(request, id):
    """
    <str:id> - document id
    """

    try:
        response = search_document_by_key(id)
        return JsonResponse(response, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({ "error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @require_POST
# def retrieve_file_details(request, id):
#     data=request.data

#     if not (data.type or data.id):
#         return JsonResponse({ "error": "Search criteria cannot be null"}, status=status.HTTP_400_BAD_REQUEST)
#     #todo: to be replaced 
#     count = 10;
#     if data.type == "like":
#         count =  count - 1
#     else:
#         count = count + 1
#     return JsonResponse({ votes: count }, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_POST
@csrf_exempt
def upvote_handler(request, id: str) -> JsonResponse:
    """
    Method POST
    JSON body
    {
        "topic": str,
        "additional_upvotes": int
    }
    
    <str:id> - document id
    """

    # validate that required fields are present
    data: dict = json.loads(request.body)
    for field in ["topic", "additional_upvotes"]:
        if data.get(field) is None:
            return JsonResponse({"error": f"missing JSON field '{field}'"},
                status=HTTPStatus.BAD_REQUEST)

    # Increment the upvotes in
    # 1) Mongo
    # 2) ElasticSearch
    new_upvote_count = upvote_document(
        topic=data["topic"],
        additional_upvotes=int(data["additional_upvotes"]), 
        id=id
    )
    
    return JsonResponse(
        {"id": id, "topic": data["topic"], "new_upvote_count": new_upvote_count},
        status=status.HTTP_200_OK
    )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_POST
@csrf_exempt
def downvote_handler(request, id: str) -> JsonResponse:
    """
    Method POST
    JSON body
    {
        "topic": str,
        "additional_downvotes": int
    }

    <str:id> - document id
    """

    # validate that required fields are present
    data: dict = json.loads(request.body)
    for field in ["topic", "additional_downvotes"]:
        if data.get(field) is None:
            return JsonResponse({"error": f"missing JSON field '{field}'"},
                status=HTTPStatus.BAD_REQUEST)

    # Increment the upvotes in
    # 1) Mongo
    # 2) ElasticSearch
    new_downvote_count = downvote_document(
        topic=data["topic"],
        additional_downvotes=int(data["additional_downvotes"]),
        id=id
    )
    
    return JsonResponse(
        {"id": id, "topic": data["topic"], "new_downvote_count": new_downvote_count}, 
        status=status.HTTP_200_OK
    )
