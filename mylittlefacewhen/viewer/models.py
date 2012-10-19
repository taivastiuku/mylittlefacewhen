import os
import random
import re
import hashlib
#import base64
from cStringIO import StringIO
from datetime import datetime, timedelta

try:    import simplejson as json
except: import json
try:    import Image
except: from PIL import Image

import requests

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail

import tagging
from resizor.restful import process_image as resizor
from viewer import forms



#IMAGESERVICE = "https://mylittlefacewhen.com/api/resizor/"
#IMAGESERVICE = "http://image.mylittlefacewhen.com/api/"
#IMAGESERVICE = "http://0.0.0.0:8001/api/"
PONIBOORU = "http://ponibooru.413chan.net/post/view/"
PONYCHAN = "http://pinkie.ponychan.net/chan/files/src/"
SIZES = ((0,100), (320,320), (640,640), (1000,1000), (1920,1920))
SIZENAMES = ("thumb", "small", "medium", "large", "huge")

PONIES = ("celestia", "molestia", "luna", "pinkie pie", "twilight sparkle", "applejack", "rarity", "fluttershy", "rainbow dash", "lyra", "bon bon", "bon bon", "rose", "sweetie belle", "spike", "scootaloo", "applebloom", "cheerilee", "big macintosh", "berry punch", "discord", "nightmare moon", "chrysalis", "cadance", "shining armor", "colgate", "silver spoon", "diamond tiara", "vinyl scratch", "derpy hooves", "hoity toity", "gummy", "snips", "snails", "spiderman", "granny smith", "opalescence", "angel", "doctor whooves", "trixie", "gilda", "skeletor")

def _detectSource(filename):
    face = filename.rpartition("/")[2]
    part = face.rpartition(".")

    if filename.lower().endswith(".gif"):
        tags = "animated, "
    else:
        tags = ""

    # ponibooru
#    if re.match("[0-9]+[ +_]-[ +_]", part[0]):
#        pid = part[0].replace("+", " ").replace("_", " ").partition(" ")[0]
#        r = requests.get(PONIBOORU + pid)
#        if r.status_code == 200:
#            source = r.content.partition("Source:")[2].partition("'")[2].partition("'")[0]
#            if not source:
#                source = PONIBOORU + pid
#            boorutags = r.content.partition("cols=50 rows=2>")[2].partition("</textarea>")[0].split()

#            for tag in boorutags:
#                tags += tag.replace("_", " ") + ", "
#
#            return (source, tags,)

    # imgur
    if len(part[0]) == 5:
        if requests.head("http://imgur.com/%s" % part[0]).status_code == 200:
            return ("http://imgur.com/%s" % part[0], tags)

    # screenshot
    elif re.match("Screenshot-S[0-9]{2}E[0-9]{2}", part[0]):
        ep = part[0].rpartition("-")[0]
        return (ep, tags + ep + ", ",)

    #DeviantART
    elif re.search("_by_[a-zA-Z0-9_]+-[a-z0-9]{7}", part[0]):
        artist = part[0].rpartition("_by_")[2].rpartition("-")[0]
        imghash = part[0].rpartition("-")[2]
        source = "http://%s.deviantart.com/#/%s" % (artist, imghash)
        return (source, tags,)

    #tumblr
    elif re.match("tumblr_", part[0]):
        return ("http://www.tumblr.com/", tags,)

    return ("",tags,)

class RandManager(models.Manager):
    """
    Adds efficent way to get randoms
    """
    def random(self, tags=None):
        if tags:
            objs = self.tagged.with_all(tag)
        else:
            objs = self.all()

        count = objs.count()
        random_index = random.randint(0, count-1)
        return objs[random_index]


class Face(models.Model):
    """
    All the reaction faces and their thumbnails.
    """
#    objects = RandManager()
    image = models.ImageField(upload_to="f/img/", default="", max_length=256)
    webp = models.ImageField(upload_to="f/thumb/", default="")
    jpg = models.ImageField(upload_to="f/thumb/", default="")
    gif = models.ImageField(upload_to="f/thumb/", default="")
    png = models.ImageField(upload_to="f/thumb/", default="")

    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    small  = models.ImageField(upload_to="f/rsz/", default="")
    medium = models.ImageField(upload_to="f/rsz/", default="")
    large  = models.ImageField(upload_to="f/rsz/", default="")
    huge   = models.ImageField(upload_to="f/rsz/", default="")

    source = models.URLField(verify_exists=False, blank=True, default="")
    md5 = models.CharField(max_length=32, default="")

    duplicate_of = models.ForeignKey('self', null=True, default=None)
    removed = models.BooleanField(default=False)
    comment = models.CharField(max_length=512, default="")

    added = models.DateTimeField('date added')

    accepted = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)

    views = models.IntegerField(default=0)

    @staticmethod
    def submit(image, tags="", source="", accepted=False):

        if image.name.lower().endswith(".gif"):
            tags = "animated, untagged, " + tags
        else:
            tags = "untagged, " + tags

        face = Face(
                added=datetime.utcnow(),
                accepted=accepted,
                source=source,
                )
        face.save()
        image.name = "mlfw" + str(face.id) + "-" + image.name
        face.image.save(image.name, image, save=True)
        face.tags = tags

        if face.generateImages():
            ChangeLog.new_edit(face)
            return face


    @staticmethod
    def exact_search(tags):
        tags_exist = True
        for tag in tags:
            if not Face.tags.filter(name=tag):
                tags_exist = False
                break

        if tags_exist:
            return Face.tagged.with_all(tags)
        else:
            return []

    @staticmethod
    def search(tags):
        tags_exist = True

        andlist = []
        anylist = [Face.tags.filter(name__contains=tag) for tag in tags if (len(unicode(tag)) > 1)]
        if not anylist:
            return []
        for l in anylist:
            andlist.append(Face.tagged.with_any(l).filter(accepted=True))
        a = set(andlist.pop(0))
        for l in andlist:
            a = a.intersection(set(l))

        return list(a)

    @staticmethod
    def random(tags=None, tag=None, number = None):
        if tag:
            objs = Face.tagged.with_all((tag,))
        elif tags:
            objs = Face.tagged.with_all(tags)
        else:
            objs = Face.objects.all()

        objs = objs.filter(accepted=True)

        count = objs.count()
        if type(number) == int:
            return [objs[random.randint(0, count-1)] for i in xrange(number)]
        else:
            return objs[random.randint(0, count-1)]

    def generateImages(self, format=None):
#        self.image.open()
        request_data = {
            #    "image":base64.b64encode(self.image.read()),
            #    "sizes":str(SIZES)[1:-1],
                "image":self.image,
                "sizes":SIZES,
                }
#        self.image.close()

        if self.image.name.rpartition(".")[2].lower() == "gif":
        #    request_data["sizes"] = str(SIZES[0])
            request_data["sizes"] = [SIZES[0]]
            request_data["write_gif"] = True

        if format:
            request_data["format"] = format
        elif not self.tags.filter(name="transparent"):
            request_data["format"] = "jpg"
        else:
            request_data["format"] = "png"


#        r = requests.post(
#                IMAGESERVICE,
#                request_data,
#                headers={"Accept-Encoding":"identity"}
#                )
#        print r.content

        resize_data = resizor(request_data)
        if not resize_data:
            return False

#        try:
#            resize_data = json.loads(r.content) #should fail if r.status_code != 200 or there is an error
#        except:
#            return False
#        resize_data = process_image(request_data)

        if resize_data.get("jpg"):
            ext = "jpg"
        elif resize_data.get("png"):
            ext = "png"
            if not self.image.name.lower().endswith(".gif"):
                tagging.models.Tag.objects.add_tag(self, "transparent")
        else:
            ext = ""

        if not ext:
            return False

        for sizename, size in zip(SIZENAMES, SIZES):
            size = json.dumps(size)
            if sizename == "thumb" and resize_data[ext].get(size):
                for e in ("jpg","png"):
                    if getattr(self, e):
                        try:
                            os.remove(getattr(self, e).path)
                        except OSError: #File not found
                            pass
                        setattr(self, e, "")

                name = "mlfw" + str(self.id) + "." + ext
                suf = SimpleUploadedFile(name,
                                         #base64.b64decode(resize_data[ext][size]),
                                         resize_data[ext][size],
                                         content_type="image/%s" % ext)
                getattr(self, ext).save(name, suf, save=False)
            elif resize_data[ext].get(size):
                if getattr(self, sizename):
                    try:
                        os.remove(getattr(self, sizename).path)
                    except OSError: #File not found
                        pass
                    setattr(self, sizename, "")
                name = "mlfw" + str(self.id) + "_" + sizename + "." + ext
                suf = SimpleUploadedFile(name,
                                         #base64.b64decode(resize_data[ext][size]),
                                         resize_data[ext][size],
                                         content_type="image/%s" % ext)
                getattr(self, sizename).save(name, suf, save=False)
        self.processed = False
        self.save()
        return True


    def accept(self):
        self.accepted = True
        self.save()

    def setThumbWithRequest(self,request):
        if request:
            webp = False
#            webp = request.webp
        else:
            webp = False
#            webp = True
        return self.setThumb(webp=webp, gif=False)


    def setThumb(self, webp=False, gif=False):
        """
        which thumbnail to show?
        """
        if self.gif and gif:
            self.thumb = self.gif
            return "gif"
        elif self.png:
            self.thumb = self.png
            return "png"
        elif webp and self.webp:
            self.thumb = self.webp
            return "webp"
        elif self.jpg:
            self.thumb = self.jpg
            return "jpg"
        else:
            self.thumb = None
            return "None"

    def get_absolute_url(self):
        """
        Not sure how this should be done.
        """
        #TODO dynamify this
        return "http://mylittlefacewhen.com/f/%d/" % self.id

    def get_image(self, size):
        img = getattr(self, size)
        if img:
            return img.url
        else:
            return self.image.url

    def age(self):
        return str(datetime.utcnow() - self.added).rpartition(":")[0]

    def public_update(self, data):
        form = forms.PublicUpdateFace(data)
        if form.is_valid():
            tags =  form.cleaned_data.get("tags")
            if tags:
                self.tags = tags
            ChangeLog.new_edit(self)
            self.save()
        else:
            print "not valid"
        return self

    def update(self, data):
        form = forms.UpdateFace(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for item in ["webp", "gif","jpg","png","huge","large","medium","small", "image"]:
                if cleaned_data.get(item):
                    if getattr(self, item):
                        try:
                            path = getattr(self, item).path
                            os.remove(path)
                        except:
                            pass
                        setattr(self, item, "")
                    getattr(self, item).save(cleaned_data[item].name, cleaned_data[item], save = False)
            for item in ["tags", "source", "processed"]:
                if cleaned_data.get(item):
                    setattr(self, item, cleaned_data[item])

            if cleaned_data.get("source") or cleaned_data.get("tags"):
                ChangeLog.new_edit(self)

            self.save()
            return True
        return False

    def remove(self, reason):
        if reason == "":
            reason = "No reason for removal was given."
        for item in ("webp", "gif", "jpg", "png", "huge", "large", "medium", "small", "image",):
            if getattr(self, item):
                try:
                    os.remove(getattr(self, item).path)
                except:
                    pass
                setattr(self, item, "")

        self.comment = reason
        self.removed = True
        self.save()

    def is_duplicate_of(self, original):
        tags = ""
        for face in (self, original):
            for tag in face.tags:
                tags += tag.name + ", "
        self.duplicate_of = original
        original.tags = tags
        self.tags = ""
        ChangeLog.new_edit(self)
        ChangeLog.new_edit(original)
        self.remove("Duplicate of id#%d" % original.id)

    def save(self, *args, **kwargs):
        self.md5 = self.md5sum()
        super(Face, self).save(*args, **kwargs)
        if (not self.height or not self.width) and self.image:
            i = Image.open(self.image.path)
            self.width = i.size[0]
            self.height = i.size[1]
            self.save()

        if self.md5 != "":
            faces = Face.objects.filter(md5=self.md5).order_by("id")
            if len(faces) > 1:
                self.is_duplicate_of(faces[0])


    def md5sum(self):
        md5 = hashlib.md5()
        try:
            with open(self.image.path, 'rb') as f:
                for chunk in iter(lambda: f.read(128*md5.block_size), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return ""

    def getMeta(self):
        """
        Artist, title and description
        """
        tags = ""
        ponies = ""
        longest = ""
        artist = None

        tagslist = [tag.name for tag in self.tags]
        tagslist.sort(key=len, reverse=True)

        for tag in tagslist:
            if tag.startswith("artist:"):
                artist = tag.partition(":")[2].strip()

            elif tag in PONIES:
                ponies += tag + ", "
            elif not longest:
                longest = tag
            else:
                tags += "'%s', " % tag


        if tags.count(",") > 1:
            tags = " and".join(tags[:-2].rsplit(",", 1)) #rrpelace()
        else:
            tags = tags[:-2]


        if ponies.count(",") > 1:
            ponies = " and".join(ponies[:-2].title().rsplit(",", 1)) #rrpelace()
        else:
            ponies = ponies[:-2].title()


        if ponies:# and longest:
            title = ponies + ": " + longest
            description = ponies + " reacting with '" + longest + "', " + tags
            if artist:
                title += " by " + artist
                description += " by " + artist
        else:
            title = "Pony Reaction Image " + str(self.id)
            description = ponies + ", " + tags + longest

        return (artist,title,description)


    def __unicode__(self):
        s = str(self.id) + " - "
        artist, title, description = self.getMeta()
        return s + title

tagging.register(Face)

class Flag(models.Model):
    """
    User can report duplicates by flagging them.
    """
    face = models.ForeignKey(Face)
    user_agent = models.CharField(max_length=512, null=True)
    reason = models.TextField()

    def save(self, *args, **kwargs):
        s = "Face:\thttp://mlfw.info/f/%s/\nReason:\t%s\nUseragent:\t%s\n" % (str(self.face.id), self.reason, self.user_agent)
        send_mail("reported! mlfw " + str(self.face.id), s, "server@mylittlefacewhen.com", ["taivastiuku@mylittlefacewhen.com", "leonard.dulitz@bronies-germany.de"])

        ret = super(Flag, self).save(*args, **kwargs)
        ChangeLog(face=self.face, flag=self).save()
        return ret


    def __unicode__(self):
        return str(self.face.id) + " - " + self.reason


class Advert(models.Model):
    htmlad = models.CharField(max_length=1024)

    @staticmethod
    def random():
        objs = Advert.objects.all()
        count = objs.count()
        return objs[ random.randint(0, count-1) ]

class Salute(models.Model):
    """
    Rainbow Salute images
    """
    filename = models.CharField(max_length=32)
    thumbnail = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    language_code = models.CharField(max_length=8)

class ChangeLog(models.Model):
    datetime = models.DateTimeField("datetime when added", auto_now=True)
    face = models.ForeignKey(Face)
    prev = models.OneToOneField("self", null=True, related_name="next")
    source = models.URLField(verify_exists=False, blank=True, default="")
    flag = models.ForeignKey(Flag, null=True)

    @staticmethod
    def new_edit(face):
        if not face.tags and not face.source:
            return

        prev = face.changelog_set.all().order_by("-datetime")
        if not prev:
            prev = None
        else:
            prev = prev[0]

            if len(prev.tags) == len(face.tags):
                same_tags = []
                for cur, pre in zip(face.tags, prev.tags):
                    if str(cur) == str(pre):
                        same_tags.append(True)
                    else:
                        same_tags.append(False)
                if all(same_tags) and prev.source == face.source:
                    #print "return"
                    return

        changelog = ChangeLog(face = face, prev=prev, source=face.source)
        changelog.save()
        tags = ""
        for tag in face.tags:
            tags += str(tag) + ","
        changelog.tags = tags
        return changelog

    def age(self):
        return str(datetime.utcnow() - self.datetime).rpartition(":")[0]

    def same(self):
        """
        What tags are shared with the previous taglog?
        """
        out = []

        if self.prev:
            for tag in self.tags:
                if tag in self.prev.tags:
                    out.append(tag)
        return out

    def removed(self):
        """
        What tags were removed from previous taglog?
        """
        out = []

        if self.prev:
            for tag in self.prev.tags:
                if tag not in self.tags:
                    out.append(tag)
        return out

    def added(self):
        """
        What tags were added from previous taglog?
        """
        out = []

        if not self.prev:
            out.extend(self.tags)
        else:
            for tag in self.tags:
                if tag not in self.prev.tags:
                    out.append(tag)
        return out


    def undo(self):
        try: self.next.public_undo()
        except: pass

        if self.source:
            if self.prev:
                self.face.source = self.prev.source
            else:
                self.face.source = ""

        if not self.prev:
            return
        else:
            tags = ""
        for tag in self.prev.tags:
            tags += tag.name + ","
        self.face.tags = tags
        self.delete()
        return True


    def __unicode__(self):
        if self.flag:
            return "Flagged with: " + self.flag.reason
        if self.prev:
            if self.prev.source != self.source:
                s = unicode(self.prev.source) + " -> " + unicode(self.source)
            else:
                s = "same source"
        else:
            s = "None -> " + unicode(self.source)
        s += " - "
        for tag in self.added():
            s += "+%s, " % unicode(tag)
        for tag in self.removed():
            s += "-%s, " % unicode(tag)
        return s[:-2]


tagging.register(ChangeLog)


class Feedback(models.Model):

    contact = models.CharField(max_length=256, default="")
    image = models.ImageField(max_length=256, upload_to="upload/")
    text = models.TextField()
    datetime = models.DateTimeField("datetime when added", auto_now_add=True)
    useragent = models.CharField(max_length=512, default="")
    processed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.text):
            s = "Contact:\t%s\nFeedback:\t%s\nTime:\t%s\nUseragent:\t%s\n" % (self.contact, self.text, str(self.datetime), self.useragent)
            send_mail("mlfw feedback: " + self.contact, s, "server@mylittlefacewhen.com", ["taivastiuku@mylittlefacewhen.com", "leonard.dulitz@bronies-germany.de"])
            return super(Feedback, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.contact + " - " + self.text

class AccessLog(models.Model):
    """
    This is used for caluclating popularity. Google Analytics doesn't see
    hotlinked traffic but Apache does.
    """
    ip = models.CharField(max_length=64)
    accessed = models.DateTimeField("access time")
    method = models.CharField(max_length=8)
    resource = models.CharField(max_length=512)
    referrer = models.CharField(max_length=1024)
    useragent = models.CharField(max_length=512)


class TagPopularity(models.Model):
    """
    Precalculated table for determining which tags are the most popular.
    How many views do pictures with given tag have.
    """
    tag = models.ForeignKey(tagging.models.Tag)
    popularity = models.IntegerField(default=0)

    def __unicode__(self):
        return self.tag.name

