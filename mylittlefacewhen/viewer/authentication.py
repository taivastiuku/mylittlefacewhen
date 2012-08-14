from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.http import HttpResponse
try:    import simplejson as json
except: import json

class Required(object):
    """
    Django authentication for piston

    This is reference implementation that requireds authentication for given 
    resource always.
    """
    request = None
    errors = None

    def is_authenticated(self, request):
        """
        if user is_authenticated: return True
        else try to autenticate with django and return true/false dependent of
        result
        """
        self.request = request

        # is authenticated
        if self.request.user.is_authenticated():
            return True

    def challenge(self):
        """
        `challenge`: In cases where `is_authenticated` returns
        False, the result of this method will be returned.
        This will usually be a `HttpResponse` object with
        some kind of challenge headers and 401 code on it.
        """
        resp = { 'error': 'Authentication needed', 'msgs': self.errors }
        return HttpResponse(json.dumps(
                resp, cls=DateTimeAwareJSONEncoder,
                ensure_ascii=False, indent=4),
            status=401,mimetype="application/json")

class AnonMethodAllowed(Required):
    """
    Allow GET for anonymous, authenticated otherwise.
    """
    allowed = []
    def set_allowed(self, allowed):
        self.allowed = allowed
        return self

    def is_authenticated(self, request):
        self.request = request

        if self.request.method in self.allowed:
            if self.request.method == "POST":
                ct = request.META.get('CONTENT_TYPE')
                if ct:
                    request.META["CONTENT_TYPE"] = ct.split(";")[0]
            return True

        # is authenticated
        if self.request.user.is_authenticated():
            return True

