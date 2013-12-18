from tastypie.authorization import Authorization


class AnonMethodAllowed(Authorization):
    allowed = []

    def set_allowed(self, allowed):
        self.allowed = allowed
        return self

    def read_list(self, object_list, bundle):
        if "GET" in self.allowed or bundle.request.user.is_superuser:
            return object_list
        else:
            return []

    def read_detail(self, object_list, bundle):
        return "GET" in self.allowed or bundle.request.user.is_superuser

    def create_detail(self, object_list, bundle):
        return "POST" in self.allowed or bundle.request.user.is_superuser

    def update_list(self, object_list, bundle):
        if "PUT" in self.allowed or bundle.request.user.is_superuser:
            return object_list
        else:
            return []

    def update_detail(self, object_list, bundle):
        return "PUT" in self.allowed or bundle.request.user.is_superuser

    def delete_list(self, object_list, bundle):
        if "DELETE" in self.allowed or bundle.request.user.is_superuser:
            return object_list
        else:
            return []

    def delete_detail(self, object_list, bundle):
        return "DELETE" in self.allowed or bundle.request.user.is_superuser
