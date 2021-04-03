from rest_framework.throttling import SimpleRateThrottle


class BasicThrottle(SimpleRateThrottle):
    rate = '100/sec'
    scope = 'all'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class StrictThrottle(SimpleRateThrottle):
    rate = '10/sec'
    scope = 'all'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }
