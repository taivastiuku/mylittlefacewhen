import json
import random
import re

#from django.core.exceptions import ObjectDoesNotExist
#from django.utils import simplejson as json
from tastypie import fields
from tastypie.api import Api
from tastypie.exceptions import BadRequest  # , NotFound
from tastypie.resources import ModelResource, Resource

from tagging.models import Tag
#from viewer import forms
from viewer import models
from viewer.api import auths
from viewer.api.validation import FaceValidation
from viewer.helpers import get_client_ip

API = Api(api_name="v3")
APIURL = "/api/v3/"
FACES_LEN = -1
MEDIA = "/media/"

fields.FileField.dehydrated_type = "file"


class PieforkModelResource(ModelResource):
    def __init__(self, **kwargs):
        super(PieforkModelResource, self).__init__(**kwargs)
        for f in getattr(self.Meta, 'readonlys', []):
            self.fields[f].readonly = True

    def build_schema(self):
        data = super(PieforkModelResource, self).build_schema()
        if hasattr(self._meta, "description"):
            data['description'] = self._meta.description
        data["contact"] = "taivastiuku@mylittlefacewhen.com"
        return data


class PieforkResource(Resource):
    def build_schema(self):
        data = super(PieforkResource, self).build_schema()
        if hasattr(self._meta, "description"):
            data['description'] = self._meta.description
        data["contact"] = "taivastiuku@mylittlefacewhen.com"
        return data


class FaceResource(PieforkModelResource):
    tags = fields.ToManyField(
        'viewer.api.v3.TagResource',
        'tags',
        full=True,
        blank=True,
        null=True,
        help_text="List of tags, input separated by comma",
        default='')

    comments = fields.ListField(
        attribute='comments',
        null=True,
        readonly=True,
        help_text="List of comments")

    artist = fields.CharField(
        attribute='artist',
        null=True,
        readonly=True,
        help_text="Name of artist of image if known")

    title = fields.CharField(
        attribute='title',
        null=True,
        readonly=True,
        help_text="Generated title for this face.")

    description = fields.CharField(
        attribute='description',
        null=True,
        readonly=True,
        help_text="Generated description for this image.")

    thumbnails = fields.DictField(
        attribute="thumbnails",
        readonly=True,
        null=True,
        help_text="List of thumbnails related to this face")

    resizes = fields.DictField(
        attribute="resizes",
        readonly=True,
        null=True,
        help_text="Resized versions of this face")

    class Meta:
        queryset = models.Face.objects.filter(removed=False)
        max_limit = 1000
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']
        always_return_data = True
        filtering = {
            "id": ["gt", "gte", "lt", "lte"],
            "accepted": ["exact"],
            "views": ["gt", "gte", "lt", "lte"],
            "hotness": ["gt", "gte", "lt", "lte"],
            "tags": ["all", "any"]}

        ordering = ["id", "random", "views", "hotness"]
        excludes = ["gif", "png", "jpg", "webp",
                    "small", "medium", "large", "huge", "removed"]
        readonlys = ["views", "md5", "accepted", "comment", "added",
                     "height", "width", "hotness", "processed"]
        authorization = auths.AnonMethodAllowed().set_allowed(
            ["GET", "POST", "PUT", "PATCH"])
        validation = FaceValidation()
        description = """Resource that contains all the reaction images in \
the service. Allows uploading base64 formatted images and modification of \
old ones. \n\
Tags should be separated by comma eg, 'yes, rainbow dash' """

#    def get_list(self, request, **kwargs):
#        trixie = request.GET.copy()
#        trixie["tags__all"] = trixie.get("tags__all", "") + ",trixie,"
#        request.GET = trixie
#        return super(FaceResource, self).get_list(request, **kwargs)

    def build_filters(self, filters=None):
        #TODO Can these be made into real filters?
        for filter in ("tags__all", "tags__any"):
            if filter in filters:
                filters.pop(filter)

        return super(FaceResource, self).build_filters(filters)

    def get_object_list(self, request):
        if request.GET.get("tags__all"):
            tagsstring = re.sub("( ?, ?)+", ",", request.GET.get("tags__all"))
            tags = tagsstring.strip(", ").split(",")
            objects = models.Face.tagged.with_all(tags)
        elif request.GET.get("tags__any"):
            tagsstring = re.sub("( ?, ?)+", ",", request.GET.get("tags__any"))
            tags = tagsstring.strip(", ").split(",")
            objects = models.Face.tagged.with_any(tags)
        else:
            objects = super(FaceResource, self).get_object_list(request)

        return objects

    def apply_sorting(self, obj_list, options=None):
        global FACES_LEN
        if options.get("order_by") in ["random", "-random"]:
            # Pseudorandom ordering because mysql random is inefficent
            limit = int(options.get("limit", 1))
            if limit > 5:
                raise BadRequest("at most 5 randoms at a time")

            obj_list = obj_list.all()
            if options.get("tags__all") or options.get("tags__any"):
                faces_len = len(obj_list)
            else:
                if FACES_LEN == -1 or random.randint(0, 1000) > 999:
                    FACES_LEN = len(obj_list)
                faces_len = FACES_LEN

            if limit >= faces_len:
                return obj_list
            else:
                i = random.randint(0, faces_len - 1 - limit)
                orders = ["id", "-id", "source", "-source", "md5", "-md5",
                          "width", "-width", "height", "-height",
                          "hotness", "-hotness", "views", "-views"]
                ordered_list = obj_list.order_by(random.choice(orders))
                return ordered_list[i:i + limit + 1]

        return super(FaceResource, self).apply_sorting(obj_list, options)

    def build_bundle(self, obj=None, data=None, request=None):
        bundle = super(FaceResource, self).build_bundle(obj, data, request)
        if request and bundle.data.get("tags"):
            tags = re.sub("( ?, ?)+", ", ", bundle.data.get("tags", "") + ", ")
            bundle.data["tags"] = tags.strip(", ")
        return bundle

    def obj_update(self, bundle, request=None, skip_errors=False, **kwargs):
        lookup_kwargs = self.lookup_kwargs_with_identifiers(bundle, kwargs)
        bundle.obj = self.obj_get(bundle, **lookup_kwargs)

        self.is_valid(bundle)

        if bundle.errors and not skip_errors:
            self.error_response(bundle.errors, request)

        bundle.obj.public_update(bundle.data)
#        if bundle.data["source"]:
#            bundle.obj.source = bundle.data["source"]

#        if bundle.data["tags"]:
#            bundle.obj.tags = bundle.data["tags"]

#        bundle.obj.save()

        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        # behavour change from 0.9 to 0.11, this is the haxfix
        bundle.data["image"] = json.dumps(bundle.data["image"])

        self.is_valid(bundle)
        if bundle.errors:
            self.error_response(request, bundle.errors)
            raise Exception()
        bundle.obj = models.Face.submit(**bundle.data)
        return bundle

API.register(FaceResource())


class UserCommentResource(PieforkModelResource):
    face = fields.ToOneField(
        'viewer.api.v3.FaceResource',
        'face',
        default="",
        help_text="id of Face related to this comment")

    class Meta:
        queryset = models.UserComment.objects.filter(visible=True)
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        ordering = ["id"]
        fields = ["username", "text", "time", "color"]
        readonlys = ["time"]
        description = """User comment on a face"""
        authorization = auths.AnonMethodAllowed().set_allowed(["POST"])

    def build_bundle(self, obj=None, data=None, request=None):
        bundle = super(UserCommentResource, self).build_bundle(obj, data, request)
        if request:
            bundle.data["client"] = get_client_ip(request)
        return bundle

    def full_hydrate(self, bundle):
        # To circumvent readonly status on client
        bundle = super(UserCommentResource, self).full_hydrate(bundle)
        bundle.obj.client = bundle.data["client"]
        return bundle

API.register(UserCommentResource())


class TagResource(PieforkModelResource):

    class Meta:
        queryset = Tag.objects.all()
        include_resource_uri = False
        max_limit = 10000
        allowed_methods = ['get']
        fields = ['name']
        filtering = {"name": ["contains", "startswith"]}
        description = """Listing of all the tags in service, can be used to \
determine what tags are available. New tags should be added straight to \
face resources."""

API.register(TagResource())


class FeedbackResource(PieforkModelResource):

    class Meta:
        queryset = models.Feedback.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        ordering = ["id"]
        excludes = ["datetime", "processed", "image"]
        readonlys = ["useragent"]
        authorization = auths.AnonMethodAllowed().set_allowed(["POST"])
        description = """Send feedback to the developers through this."""

    def build_bundle(self, obj=None, data=None, request=None):
        bundle = super(FeedbackResource, self).build_bundle(obj, data, request)
        if request:
            bundle.data["useragent"] = request.META.get("HTTP_USER_AGENT")
        return bundle

    def full_hydrate(self, bundle):
        # To circumvent readonly status on useragent
        bundle = super(FeedbackResource, self).full_hydrate(bundle)
        bundle.obj.useragent = bundle.data["useragent"]
        return bundle

API.register(FeedbackResource())


class DetectResource(PieforkResource):

    filename = fields.CharField(help_text="Filename of a file.")

    class Meta:
        include_resource_uri = False
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        description = """Try to detect source and tags from filename."""

    def get_object_list(self, *args, **kwargs):
        return []

    def get_list(self, request=None, **kwargs):
        filename = request.GET.get("filename")
        if filename:
            source, tags = models._detectSource(filename)
        else:
            raise BadRequest("'filename' is required parameter")
        return self.create_response(request, {"source": source, "tags": tags})

API.register(DetectResource())


class FlagResource(PieforkModelResource):

    face = fields.ToOneField(
        'viewer.api.v3.FaceResource',
        'face',
        default="",
        help_text="id of Face related to this report")

    class Meta:
        queryset = models.Flag.objects.all()
        include_resource_uri = False
        ordering = ["id"]
        authorization = auths.AnonMethodAllowed().set_allowed(["POST"])
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        readonlys = ["user_agent"]
        description = """Flag face resource due to inappropriate content, \
poor quality, duplicate or other reason."""

    def build_bundle(self, obj=None, data=None, request=None):

        bundle = super(FlagResource, self).build_bundle(obj, data, request)

#        if type(data.get("face")) is dict:
#            raise BadRequest("Suspicious operation")
#        else:
#            try:
#                id = int(bundle.data["face"])
#                bundle.data["face"] = APIURL + "face/%d/" % id
#            except:
#                pass
        if request:
            useragent = request.META.get("HTTP_USER_AGENT")
            bundle.data["user_agent"] = useragent
            if not bundle.data.get("face"):
                referer = request.META.get("HTTP_REFERER")
                bundle.data["face"] = referer.strip("/")
        return bundle

    def full_hydrate(self, bundle):
        # To circumvent readonly status on useragent
        bundle = super(FlagResource, self).full_hydrate(bundle)
        bundle.obj.user_agent = bundle.data["user_agent"]
        return bundle


API.register(FlagResource())


class AdResource(PieforkModelResource):

    class Meta:
        queryset = models.Advert.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        include_resource_uri = False
        description = """Random advertisements show on the service."""

    def apply_sorting(self, obj_list, options=None):
        i = random.randint(0, len(obj_list) - 1)
        return obj_list[i:i + 1]

API.register(AdResource())
