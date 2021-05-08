from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "OK"})
