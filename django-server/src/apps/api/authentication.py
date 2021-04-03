from django.conf import settings
from rest_framework.authentication import (
        get_authorization_header, BaseAuthentication)
from rest_framework.exceptions import PermissionDenied


class BasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # do not authenticate if request is pre-flight in case of CORS
        if request.method == 'OPTIONS':
            return

        base_token = settings.API_AUTH_TOKEN
        token_from_get_param = request.GET.get('token')
        if (settings.DEV and token_from_get_param is not None
                and token_from_get_param == base_token):
            return

        auth = get_authorization_header(request).split()
        token_key = 'Bearer'.encode()
        token = base_token.encode()
        if len(auth) == 2 and auth[0] == token_key and auth[1] == token:
            return

        raise PermissionDenied()
