from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services.search_service import search_documents

# Create your views here.


@require_GET
def search(request):
    search_string = request.GET.get("query")

    if search_string:
        try:
            response = search_documents(search_string)
            return JsonResponse(response)
        except Exception:
            return JsonResponse({"Status": 500, "Error": "Internal Server Error"})

    else:
        return JsonResponse({"Status": 400, "Error": "Bad Request"})
