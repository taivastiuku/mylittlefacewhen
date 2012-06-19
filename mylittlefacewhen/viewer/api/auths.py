from tastypie.authorization import Authorization

class AnonMethodAllowed(Authorization):
    allowed = []
    def set_allowed(self, allowed):
        self.allowed = allowed
        return self

    def is_authorized(self, request, object=None):
        if request.method in self.allowed:
            return True
        if request.user.is_authenticated():
            return True
        return False
