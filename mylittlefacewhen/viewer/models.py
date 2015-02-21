#from cStringIO import StringIO
from datetime import datetime
import hashlib
import json
import os
import random
import re

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail

try:
    import Image
except:
    from PIL import Image  # NOQA

import requests
import tagging

from resizor.restful import process_image as resizor
from viewer import forms

#IMAGESERVICE = "https://mylittlefacewhen.com/api/resizor/"
#IMAGESERVICE = "http://image.mylittlefacewhen.com/api/"
#IMAGESERVICE = "http://0.0.0.0:8001/api/"
PONIBOORU = "http://ponibooru.413chan.net/post/view/"
PONYCHAN = "http://pinkie.ponychan.net/chan/files/src/"
SIZES = ((0, 100), (320, 320), (640, 640), (1000, 1000), (1920, 1920))
SIZENAMES = ("thumb", "small", "medium", "large", "huge")

PONIES = {
    "celestia", "molestia", "luna", "pinkie pie", "twilight sparkle", "applejack", "rarity", "fluttershy",
    "rainbow dash", "lyra", "bon bon", "bon bon", "rose", "sweetie belle", "spike", "scootaloo", "applebloom",
    "cheerilee", "big macintosh", "berry punch", "discord", "nightmare moon", "chrysalis", "cadance",
    "shining armor", "colgate", "silver spoon", "diamond tiara", "vinyl scratch", "derpy hooves", "hoity toity",
    "gummy", "snips", "snails", "spiderman", "granny smith", "opalescence", "angel", "doctor whooves", "trixie",
    "gilda", "skeletor", "octavia", "lauren faust", "daring do", "guard pony", "ursa minor", "lightning dust",
    "zecora"}

#TODO all episodes
#TODO tags should cointain info about the character without sets like these

CMC = {"scootaloo", "applebloom", "sweetie belle"}
MANE6 = {"twilight sparkle", "pinkie pie", "rainbow dash", "fluttershy", "rarity", "applejack"}

ADMINMAILS = ["moderators@mylittlefacewhen.com"]


def _detectSource(filename):
    face = filename.rpartition("/")[2]
    part = face.rpartition(".")

    if filename.lower().endswith(".gif"):
        tags = "animated, "
    else:
        tags = ""

    # imgur
    if len(part[0]) == 5:
        if requests.head("http://imgur.com/%s" % part[0]).status_code == 200:
            return ("http://imgur.com/%s" % part[0], tags)

    # screenshot
    elif re.match("Screenshot-S[0-9]{2}E[0-9]{2}", part[0]):
        ep = part[0].rpartition("-")[0]
        return (ep, tags + ep + ", ")

    #DeviantART
    elif re.search("_by_[a-zA-Z0-9_]+-[a-z0-9]{7}", part[0]):
        artist = part[0].rpartition("_by_")[2].rpartition("-")[0]
        imghash = part[0].rpartition("-")[2]
        source = "http://%s.deviantart.com/#/%s" % (artist, imghash)
        return (source, tags)

    #tumblr
    elif re.match("tumblr_", part[0]):
        return ("http://www.tumblr.com/", tags)

    return ("", tags)


class RandManager(models.Manager):
    """
    Adds efficent way to get randoms
    """
    def random(self, tags=None):
        if tags:
            objs = self.tagged.with_all(tags)
        else:
            objs = self.all()

        count = objs.count()
        random_index = random.randint(0, count - 1)
        return objs[random_index]


class Face(models.Model):
    """
    All the reaction faces and their thumbnails.
    """
#    objects = RandManager()
    image = models.ImageField(
        upload_to="f/img/",
        default="",
        max_length=256,
        help_text="Image uploaded in base64 format. The core of this service.")

    # THUMBNAILS
    webp = models.ImageField(
        upload_to="f/thumb/",
        default="",
        blank=True,
        help_text="WEBP formatted thumbnail, max height: 100px")

    jpg = models.ImageField(
        upload_to="f/thumb/",
        default="",
        blank=True,
        help_text="JPG formatted thumbnail, max height: 100px")

    gif = models.ImageField(
        upload_to="f/thumb/",
        default="",
        blank=True,
        help_text="animated GIF thumbnail, max height: 100px")

    png = models.ImageField(
        upload_to="f/thumb/",
        default="",
        blank=True,
        help_text="transparent PNG thumbnail, max height: 100px")

    # RESIZES
    small = models.ImageField(
        upload_to="f/rsz/",
        default="",
        blank=True,
        help_text="Resize of image fitted into 320x320 box")

    medium = models.ImageField(
        upload_to="f/rsz/",
        default="",
        blank=True,
        help_text="Resize of image fitted into 640x640 box")

    large = models.ImageField(
        upload_to="f/rsz/",
        default="",
        blank=True,
        help_text="Resize of image fitted into 1000x1000 box")

    huge = models.ImageField(
        upload_to="f/rsz/",
        default="",
        blank=True,
        help_text="Resize of image fitted into 1920x1920 box")

    # META-DATA
    width = models.IntegerField(
        default=0,
        help_text="Width of image")

    height = models.IntegerField(
        default=0,
        help_text="Height of image")

    source = models.URLField(
        # verify_exists=False,
        blank=True,
        default="",
        help_text="Source for image")

    md5 = models.CharField(
        max_length=32,
        default="",
        help_text="md5 hash of image for detecting duplicates.")

    duplicate_of = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        help_text="Current image is duplicate, redirect to duplicate_of Face")

    removed = models.BooleanField(
        default=False,
        help_text="Image is 'removed' and should not be shown")

    comment = models.CharField(
        max_length=512,
        blank=True,
        default="",
        help_text="Reason for deletion etc.")

    added = models.DateTimeField(
        'date added',
        help_text="Date added")

    accepted = models.BooleanField(
        default=False,
        help_text="Face has been accepted by moderator.")

    processed = models.BooleanField(
        default=False,
        help_text="Thumbnails and resizes have been generated and compressed")

    views = models.IntegerField(
        default=0,
        help_text="Views during last 7 days.")

    hotness = models.FloatField(
        default=0,
        help_text="Represents newness and popularity of face.")

    IMAGEFIELDS = ("webp", "gif", "jpg", "png",
                   "huge", "large", "medium", "small", "image")

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

#    @staticmethod
#    def search(tags):
#        #tags_exist = True

#        andlist = []
#        anylist = [Face.tags.filter(name__contains=tag) for tag in tags if (len(unicode(tag)) > 1)]
#        if not anylist:
#            return []
#        for l in anylist:
#            andlist.append(Face.tagged.with_any(l).filter(accepted=True))
#        a = set(andlist.pop(0))
#        for l in andlist:
#            a = a.intersection(set(l))
#
#        return list(a)

    @staticmethod
    def random(tags=None, tag=None, number=None):
        if tag:
            objs = Face.tagged.with_all((tag,))
        elif tags:
            objs = Face.tagged.with_all(tags)
        else:
            objs = Face.objects.all()

        objs = objs.filter(accepted=True)

        count = objs.count()
        if type(number) == int:
            return [objs[random.randint(0, count - 1)] for i in xrange(number)]
        else:
            return objs[random.randint(0, count - 1)]

    @property
    def comments(self):
        out = []
        for item in self.usercomment_set.filter(visible="visible").order_by("-time"):
            out.append({"username": item.username, "text": item.safe_text, "color": item.color})

        return out

    def generateImages(self, format=None):
        # self.image.open()
        request_data = {
            # "image": base64.b64encode(self.image.read()),
            # "sizes": str(SIZES)[1:-1],
            "image": self.image,
            "sizes": SIZES,
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
#            # should fail if r.status_code != 200 or there is an error
#            resize_data = json.loads(r.content)
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
                for e in ("jpg", "png"):
                    if getattr(self, e):
                        try:
                            os.remove(getattr(self, e).path)
                        except OSError:  # File not found
                            pass
                        setattr(self, e, "")

                name = "mlfw" + str(self.id) + "." + ext
                suf = SimpleUploadedFile(
                    name,
                    # base64.b64decode(resize_data[ext][size]),
                    resize_data[ext][size],
                    content_type="image/%s" % ext)
                getattr(self, ext).save(name, suf, save=False)
            elif resize_data[ext].get(size):
                if getattr(self, sizename):
                    try:
                        os.remove(getattr(self, sizename).path)
                    except OSError:  # File not found
                        pass
                    setattr(self, sizename, "")
                name = "mlfw" + str(self.id) + "_" + sizename + "." + ext
                suf = SimpleUploadedFile(
                    name,
                    # base64.b64decode(resize_data[ext][size]),
                    resize_data[ext][size],
                    content_type="image/%s" % ext)
                getattr(self, sizename).save(name, suf, save=False)
        self.processed = False
        self.save()
        return True

    def accept(self):
        self.accepted = True
        self.save()

    def setThumbWithRequest(self, request):
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
            tags = form.cleaned_data.get("tags")
            source = form.cleaned_data.get("source")
            #print form.cleaned_data
            if tags:
                self.tags = tags

            if source:
                self.source = source

            ChangeLog.new_edit(self)
            self.save()
            #print self.source
            #print self.tags
        else:
            pass
            #print "not valid"
        return self

    def update(self, data):
        form = forms.UpdateFace(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for item in self.IMAGEFIELDS:
                if cleaned_data.get(item):
                    if getattr(self, item):
                        try:
                            path = getattr(self, item).path
                            os.remove(path)
                        except:
                            pass
                        setattr(self, item, "")
                    getattr(self, item).save(
                        cleaned_data[item].name,
                        cleaned_data[item],
                        save=False)

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
        for item in self.IMAGEFIELDS:
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

    def update_comments(self):
        older_comments = self.usercomment_set.filter(visible="visible").order_by("-time")
        if older_comments.count() > 10:
            oldest_to_show = older_comments[9].id
            to_hide = self.usercomment_set.filter(id__lt=oldest_to_show, visible="visible")
            to_hide.update(visible="hidden")

    def md5sum(self):
        # http://stackoverflow.com/questions/1131220/
        md5 = hashlib.md5()
        try:
            with open(self.image.path, 'rb') as f:
                for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except:
            return ""

    def getMeta(self):
        """
        Artist, title and description
        """
        tags = []
        ponies = set()
        longest = ""
        artist = None

        tagslist = [tag.name for tag in self.tags]
        tagslist.sort(key=len, reverse=True)

        def rreplace(string, old, new, maxNumber=1):
            # replace from right
            return new.join(string.rsplit(old, maxNumber))

        for tag in tagslist:
            if tag.startswith("princess "):
                tag = tag[9:]

            if tag.startswith("artist:"):
                artist = tag.partition(":")[2].strip()

            elif tag in PONIES:
                ponies.add(tag)
            elif not longest and tag not in {"untagged", "transparent", "screenshot", "animated", "fanart", "caption"}:
                longest = tag
                tags.insert(0, longest)
            else:
                tags.append(tag)

        tags.append("my little pony")

        for ponyset, setname in [(CMC, "cutie mark crusaders"), (MANE6, "mane 6")]:
            if ponies.issuperset(ponyset):
                for item in ponyset:
                    ponies.remove(item)
                ponies.add(setname)

        tags = "'%s'" % rreplace("', '".join(tags), ",", " and")
        ponies = rreplace(", ".join(ponies).title(), ",", " and")
        if not ponies:
            ponies = "Pony reaction"

        title = ponies + ": " + longest
        description = ponies + " reacting with " + tags
        if artist:
            title += " by " + artist
            description += " by " + artist

        return (artist, title, description)

    @property
    def artist(self):
        if not hasattr(self, "_metadata"):
            self._metadata = self.getMeta()
        return self._metadata[0]

    @property
    def title(self):
        if not hasattr(self, "_metadata"):
            self._metadata = self.getMeta()
        return self._metadata[1]

    @property
    def description(self):
        if not hasattr(self, "_metadata"):
            self._metadata = self.getMeta()
        return self._metadata[2]

    @property
    def thumbnail(self):
        if not hasattr(self, "thumb"):
            self.setThumb(gif=True)
        return self.thumb

    @property
    def taglist(self):
        return ", ".join([tag.name for tag in self.tags])

    @property
    def thumbnails(self):
        thumbnails = {}
        for format in ("png", "jpg", "webp", "gif"):
            img = getattr(self, format)
            if img:
                thumbnails[format] = img.url
        return thumbnails

    @property
    def resizes(self):
        resizes = {}
        for size in ("small", "medium", "large", "huge"):
            resize = getattr(self, size)
            if resize:
                resizes[size] = resize.url

        return resizes

    def __unicode__(self):
        return str(self.id) + " - " + self.title

tagging.register(Face)


class Flag(models.Model):
    """
    User can report duplicates by flagging them.
    """
    face = models.ForeignKey(
        Face,
        help_text="Face related to this report.")

    user_agent = models.CharField(
        max_length=512,
        null=True,
        help_text="User agent of reporter.")

    reason = models.TextField(
        help_text="Reason for report.")

    def save(self, *args, **kwargs):
        s = "Face:\thttp://mlfw.info/f/%s/\nReason:\t%s\nUseragent:\t%s\n" % \
            (str(self.face.id), self.reason, self.user_agent)
        send_mail(
            "reported! mlfw " + str(self.face.id),
            s,
            "server@mylittlefacewhen.com",
            ADMINMAILS)

        ret = super(Flag, self).save(*args, **kwargs)
        ChangeLog(face=self.face, flag=self).save()
        return ret

    def __unicode__(self):
        return str(self.face.id) + " - " + self.reason


class Advert(models.Model):
    htmlad = models.CharField(
        max_length=1024, help_text="Advertisement text, may contain html.")

    @staticmethod
    def random():
        objs = Advert.objects.all()
        count = objs.count()
        return objs[random.randint(0, count - 1)]


class ChangeLog(models.Model):
    datetime = models.DateTimeField(
        "datetime when added",
        auto_now=True,
        help_text="Datetime of change")

    face = models.ForeignKey(
        Face,
        help_text="Face related to change")

    source = models.URLField(
        # verify_exists=False,
        blank=True,
        default="",
        help_text="New source for face")

    flag = models.ForeignKey(
        Flag,
        null=True,
        help_text="Face was flagged",
        on_delete=models.SET_NULL)

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

        changelog = ChangeLog(face=face, source=face.source)
        changelog.save()
        tags = ""
        for tag in face.tags:
            tags += str(tag) + ","
        changelog.tags = tags
        return changelog

    @property
    def age(self):
        return str(datetime.utcnow() - self.datetime).rpartition(":")[0]

    @property
    def same_tags(self):
        return ", ".join([tag.name for tag in self.same()])

    @property
    def removed_tags(self):
        return ", ".join([tag.name for tag in self.removed()])

    @property
    def added_tags(self):
        return ", ".join([tag.name for tag in self.added()])

    @property
    def source_change(self):
        if self.prev:
            if self.source != self.prev.source:
                return self.prev.source + " -> " + self.source
            else:
                return ""
        else:
            return self.source

    @property
    def prev(self):
        if not hasattr(self, "_prev"):
            try:
                self._prev = self.face.changelog_set.filter(datetime__lt=self.datetime).order_by("-datetime")[0]
            except:
                self._prev = None
        return self._prev

    def same(self):
        """
        What tags are shared with the previous taglog?
        """
        out = []

        if self.prev is not None:
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
        if self.prev:
            self.face.source = self.prev.source
            self.face.save()
        else:
            self.face.tags = ""
            self.delete()
            return

        tags = set([tag.name for tag in self.face.tags])
        for tag in self.removed():
            tags.add(tag.name)

        for tag in self.added():
            try:
                tags.remove(tag.name)
            except:
                pass

        self.face.tags = ", ".join(tags)
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
    contact = models.CharField(
        max_length=256,
        default="",
        help_text="Contact info of feedback giver")

    image = models.ImageField(
        max_length=256,
        upload_to="upload/",
        help_text="DEPRECATED")

    text = models.TextField(
        help_text="The feedback goes here. What is on your mind?")

    datetime = models.DateTimeField(
        "datetime when added",
        auto_now_add=True,
        help_text="When the feedback was received.")

    useragent = models.CharField(
        max_length=512,
        default="",
        help_text="Useragent of feedback giver. Useful for bug reports.")

    processed = models.BooleanField(
        default=False,
        help_text="DEPRECATED")

    def save(self, *args, **kwargs):
        if (self.text):
            s = "Contact:\t%s\nFeedback:\t%s\nTime:\t%s\nUseragent:\t%s\n" % \
                (self.contact, self.text, str(self.datetime), self.useragent)
            send_mail(
                "mlfw feedback: " + self.contact,
                s,
                "server@mylittlefacewhen.com",
                ADMINMAILS)
            return super(Feedback, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.contact + " - " + self.text


class UserComment(models.Model):
    VISIBILITY = (
        ("moderated", "Moderated"),
        ("hidden", "Hidden"),
        ("visible", "Visible"))

    face = models.ForeignKey(
        Face,
        help_text="Face that is being commented")

    username = models.CharField(
        max_length=16,
        default="Poninymous",
        help_text="Username of anon user")

    text = models.CharField(
        max_length=255,
        default="",
        help_text="Comment itself")

    client = models.IPAddressField(
        help_text="IP of the commenter")

    visible = models.CharField(
        max_length=16,
        choices=VISIBILITY,
        default="visible",
        help_text="If comment is visible, moderated or hidden")

    color = models.CharField(
        max_length=6,
        help_text="IP/Face specific color")

    time = models.DateTimeField(
        auto_now_add=True,
        help_text="Time of writing")

    @property
    def safe_text(self):
        text = self.text.split(" ")
        out = []
        for word in text:
            if len(word) > 30:
                parts = []
                l = 10
                for j in range(0, len(word) / l):
                    parts.append(word[j * l: (j + 1) * l])
                word = u"\u200B".join(parts)
            out.append(word)
        return u" ".join(out)

    def save(self, *args, **kwargs):

        #TODO do validation in a form
        if self.text.strip() == "" or self.username.strip() == "":
            return False

        """Only 10 newest comments are shown."""
        previous_comments = UserComment.objects.filter(face=self.face, client=self.client)

        if previous_comments:
            self.color = previous_comments[0].color
        elif not self.color:
            def get_color():
                colors = []
                for _ in range(0, 3):
                    if not random.randint(0, 2):
                        colors.append("cc")
                    else:
                        colors.append(str(hex(random.randint(0x00, 0x99))[2:]).zfill(2))
                colors = "".join(colors)
               # print colors, colors == "ffffff"
                if colors == "aaaaaa":
                    return get_color()
                else:
                    return colors

            self.color = get_color()

        self.face.update_comments()

        return super(UserComment, self).save(*args, **kwargs)
