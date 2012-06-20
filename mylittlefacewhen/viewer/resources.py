from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import get_object_or_404
from piston.handler import BaseHandler
from piston.utils import validate, rc
from viewer import models
from viewer import forms
from tagging.models import Tag
import tagging
import base64
import random
import re

import json
from datetime import datetime

#IMAGEURL = "http://images.mlfw.info"
IMAGEURL = "http://images.mylittlefacewhen.com"
#IMAGEURL = "http://mylittlefacewhen.com"
SERVICEURL = "http://mylittlefacewhen.com"

def limit_and_order(function):
    def decorator(handler, request, *args, **kvargs):
        DEFAULT_LIMIT = 30
        MAX_LIMIT = 1000
        request.order = request.GET.get("order", None)
        limit = request.GET.get("limit", None)

        if request.order == "random" and not limit:
            request.limit = 1

        elif limit:
            try:
                limit = int(limit)
                if limit < 1 or limit > MAX_LIMIT:
                    ret = rc.BAD_REQUEST
                    ret.write(": limit should be between 1 and %d" % MAX_LIMIT)
                    return ret
                request.limit = limit
            except:
                ret = rc.BAD_REQUEST
                ret.write(": Integer limits only")
                return ret
        else:
            request.limit = DEFAULT_LIMIT

        return function(handler, request, *args, **kvargs)
    return decorator

class FaceHandler(BaseHandler):
    """
    base class for models.Face handlers
    """
    model = models.Face
    
    fields = ('link', 'shortlink', 'image', 'thumbnails', 'accepted', 'processed', 'views', 'tags', 'id', 'resizes', 'source', 'width', 'height')

    @staticmethod
    def tags(instance):
        return [str(tag) for tag in instance.tags]

    @staticmethod
    def link(instance):
        return "http://mylittlefacewhen.com/f/%d/" % instance.id

    @staticmethod
    def shortlink(instance):
        return "http://mlfw.info/f/%d/" % instance.id

    @staticmethod
    def image(instance):
        if instance.image:
            if instance.accepted:
                return IMAGEURL + instance.image.url
            else:
                return SERVICEURL + instance.image.url
        else:
            return ""

    @staticmethod
    def thumbnails(instance):
        out = {}
        for thumb in ("webp", "png", "jpg", "gif"):
            if getattr(instance, thumb):
                if instance.accepted:
                    out[thumb] = IMAGEURL + getattr(instance, thumb).url
                else:
                    out[thumb] = SERVICEURL + getattr(instance, thumb).url
        return out

    @staticmethod
    def resizes(instance):
        out = {}
        for rsz in ("huge", "large", "medium", "small"):
            if getattr(instance, rsz):
                if instance.accepted:
                    out[rsz] = IMAGEURL + getattr(instance, rsz).url
                else:
                    out[rsz] = SERVICEURL + getattr(instance, rsz).url
        return out


class FacesHandler(FaceHandler):
    """
    Fetch face by id, fetch faces by page or create faces.
    """
    allowed_method = ('GET', 'POST', 'PUT', 'DELETE',)

    @limit_and_order
    def read(self, request, uid=None):

        base = self.model.objects

        if uid:
            return get_object_or_404(self.model, pk=uid)
        elif request.GET.get("unprocessed"):
            return base.filter(processed=False).order_by("-id")
        elif request.GET.get("accepted"):
            return base.filter(accepted=False).order_by("-id")
        elif request.GET.get("tags"):
            tags = json.loads(request.GET.get("tags"))
            faces = list(self.model.exact_search(tags))
            if not faces:
                faces = self.model.search(tags)

            if request.order == "random":
               random.shuffle(faces)
            return faces[0:request.limit]

        else:
        
            try:
                page = int(request.GET.get("page"))
            except:
                page = 1
            
            if request.order not in ("-id","id","-views","views", "random", None):
                ret = rc.BAD_REQUEST
                ret.write(""": order should be in ("-id","id","-views","views", "random")""")
                return ret
            if request.order == None:
                request.order = "id"

            offset = (page - 1) * request.limit
            if request.order == "random":
                return models.Face.random(number=request.limit)
            else:
                return base.filter(accepted=1).order_by(request.order)[0 + offset:request.limit + offset]

    @validate(forms.CreateFace)
    def create(self, request):
#        if request.user.is_authenticated():
#            request.form.accepted = True
        return self.model.submit(**request.form.cleaned_data)

    def update(self, request, uid=None):
        face = get_object_or_404(self.model, pk=uid)

        if request.user.is_authenticated():
            if not request.PUT:
                face.accept()
            elif request.PUT.get("generateImages"):
                face.generateImages()
            else:
                post = request.POST.copy()
                post["uid"] = uid
                if not face.update(post):
                    ret = rc.BAD_REQUEST
                    ret.write(""": something went wrong""")
                    return ret
            return face
        else:
            try:
                put = json.loads(request.raw_post_data)
                tags = ""
                for tag in put["tags"]:
                    tags += tag + ", "
                put = {
                        "tags": tags,
                        "source": put["source"],
                        }
            except:
                ret = rc.BAD_REQUEST
                ret.write(""": something went wrong""")
                return ret

            face.public_update(put)
        return face
            
    def delete(self, request, uid=None):
        face = get_object_or_404(self.model, pk=uid)
        if face.accepted == False:
            face.delete()
            return True
        else:
            return False


class LoginHandler(BaseHandler):
    """
    Some resources need authentication.
    """
    allowed_method = ('POST',)
    def create(self,request):
        # not authenticated, call authentication form
        f = AuthenticationForm(data={
            'username': request.POST.get('username',''),
            'password': request.POST.get('password',''),
        })

        # if authenticated log the user in.
        if f.is_valid():

            auth_login(request,f.get_user())
            # this ** should ** return true
            return request.user.is_authenticated()

        else:
            ret = rc.FORBIDDEN
            ret.write(": I don't know you.")
            return ret
            
    
class SearchHandler(FaceHandler):
    """
    Search faces with a list of keywords. 1 char words disregarded, partial results are accepted for the rest.
    """
    allowed_method = ('GET', )

    @limit_and_order
    def read(self, request):
        try:
            tags = request.GET.get("tags")
            tags = json.loads(request.GET.get("tags"))
            for index, value in enumerate(tags):
                tags[index] = value.strip()

        except:
            ret = rc.BAD_REQUEST
            ret.write(": No search tags or invalid tags.")
            return ret

        faces = list(self.model.exact_search(tags))
        if not faces:
            faces = self.model.search(tags)

        if request.order == "random":
           random.shuffle(faces)
        return faces[0:request.limit]


class TagsHandler(BaseHandler):
    allowed_method = ('GET', )
    model = tagging.models.Tag
    
    def read(self, request):
        term = request.GET.get("term")
        mode = request.GET.get("mode")
        if mode not in ("startswith", "models") and mode:
            ret = rc.BAD_REQUEST
            ret.write(": Invalid mode. Use 'startswith' or don't supply at all.")
            return ret

        if term and mode == "startswith":
            tags = models.Face.tags.filter(name__startswith=term)
        elif term:
            tags = models.Face.tags.filter(name__contains=term)
        elif mode == "models":
            return models.Face.tags.all()
        else: 
            tags = models.Face.tags.all()

        return [str(tag) for tag in tags]

class FeedbackHandler(BaseHandler):
    """
    Allows posting, reading and marking as read of feedback.
    """
    allowed_method = ('GET', 'POST', 'PUT')
    model = models.Feedback
    fields = ('id', 'contact', 'image', 'text', 'datetime','processed')

    @staticmethod
    def image(instance):
        try:
            return "http://mylittlefacewhen.com" + instance.image.url
        except:
            return ""

    def read(self, request, uid=None):
        """
        Authenticatd
        For easy access to feedback
        """
        if uid:
            return get_object_or_404(self.model, pk = uid)
        else:
            return self.model.objects.all().order_by('datetime')

    def create(self, request, uid=None):
        """
        3rd party can send messages with this. No image uploading currently.
        """
        try:
            post = json.loads(request.raw_post_data)
            feedback = post["feedback"]
            contact = post.get("contact", "")
        except:
            ret = rc.BAD_REQUEST
            ret.write(": no 'feedback' was received")
            return ret
        fb = self.model(text=feedback, datetime=datetime.utcnow(), contact=contact)
        fb.save()
        return {"success":"Thanks for your feedback!"}

    def update(self, request, uid=None):
        """
        Authenticated
        Marks feedback read/unread by given id.
        """
        feedback = get_object_or_404(self.model, pk = uid)
        try:
           feedback.processed = bool(request.POST["processed"])
        except:
           feedback.processed = not feedback.processed
        feedback.save()
        return feedback


class DetectHandler(BaseHandler):
    allowed_method = ('GET', )
    
    def read(self, request):
        filename = request.GET.get("filename")
        if filename:
            #print filename
            source, tags = models._detectSource(filename)
        else:
            ret = rc.BAD_REQUEST
            ret.write(": no 'filename' was received")
            return ret
        return {"source":source, "tags": tags, }


class ReportHandler(BaseHandler):
    allowed_method = ("POST",)

    def create(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        face_id = request.META.get("HTTP_REFERER")
        report = request.POST.get("report")
        if not all((face_id, report)):
            ret = rc.BAD_REQUET
            ret.write(": referer or report not included")
            return ret

        for part in face_id.split("/"):
            try:
                face_id = int(part)
                break
            except:
                continue

        try:
            face = models.Face.objects.get(id=int(face_id))
        except:
            ret = rc.BAD_REQUET
            ret.write(": couldn't detect the page you're on")
            return ret

        flag = models.Flag(
                face=face,
                user_agent=user_agent, 
                reason=report
                )
        flag.save()

        return flag

