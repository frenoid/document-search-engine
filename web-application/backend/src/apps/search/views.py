from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_GET, require_POST
from .services.search_service import search_documents, search_document_by_key
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
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
    file_id = self.kwargs['id']
    print(file_id)
    if file_id:
        try:
            response = search_document_by_key(file_id)
            return JsonResponse(response, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({ "error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({ "error": "Search criteria cannot be null"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_POST
def retrieve_file_details(request, id):
    data=request.data

    if not (data.type or data.id):
        return JsonResponse({ "error": "Search criteria cannot be null"}, status=status.HTTP_400_BAD_REQUEST)
    #todo: to be replaced 
    count = 10;
    if data.type == "like":
        count =  count - 1
    else:
        count = count + 1
    return JsonResponse({ votes: count }, status=status.HTTP_200_OK)

