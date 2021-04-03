from django.conf import settings


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        allowed_headers = 'Origin, Content-Type, Authorization'
        response['Access-Control-Allow-Origin'] = settings.CORS
        response['Access-Control-Allow-Headers'] = allowed_headers
        return response
