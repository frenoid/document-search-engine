from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_GET
from .services.search_service import search_documents
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# Create your views here.

@permission_classes([IsAuthenticated])
@require_GET
def search(request):
    search_string = request.GET.get("search")

    if search_string:
        try:
            response = search_documents(search_string)
            return JsonResponse(content=response, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({ "error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({ "error": "Search criteria cannot be null"}, status=status.HTTP_400_BAD_REQUEST)
