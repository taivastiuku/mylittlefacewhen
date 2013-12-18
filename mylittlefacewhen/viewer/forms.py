import base64
import json

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

#mokeypatch
#old_build_attrs = forms.Widget.build_attrs
#def build_attrs(self, extra_attrs=None, **kwargs):
#  attrs = old_build_attrs(self, extra_attrs, **kwargs)
#
#  if self.is_required:
#    attrs["required"] = "required"
#
#  return attrs
#
#forms.Widget.build_attrs = build_attrs


class FeedbackForm(forms.Form):
    """
    Feedback
    """
    contact = forms.CharField(label="Contact", required=False, max_length=256)
    #file = forms.ImageField(label="File", required=False)
    text = forms.CharField(
        label="Feedback*",
        required=True,
        widget=forms.Textarea
    )
    useragent = forms.CharField(widget=forms.HiddenInput(), required=False)


class Flag(forms.Form):
    face = forms.CharField(required=False)
    reason = forms.CharField()
    user_agent = forms.CharField(required=False)


class PublicUpdateFace(forms.Form):
    source = forms.CharField(max_length=256, required=False)
    tags = forms.CharField(max_length=1024, required=False)

    def clean(self):
        data = self.cleaned_data
        if not data.get("source") and not data.get("tags"):
            raise forms.ValidationError("No data supplied")

        return data

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        if tags == "":
            return ""
        tags = tags.strip(" ,") + ","
        if not tags.find("http://") == -1:
            raise forms.ValidationError("No links allowed in tags")
        return tags


class UpdateFace(forms.Form):
    """
    This is used by the api for validation.
    """
    uid = forms.IntegerField(required=True)
    name = forms.CharField(max_length=240, required=False)
    image = forms.CharField(max_length=10000000, required=False)
    webp = forms.CharField(max_length=15000, required=False)
    jpg = forms.CharField(max_length=15000, required=False)
    png = forms.CharField(max_length=20000, required=False)
    gif = forms.CharField(max_length=5000000, required=False)
    tags = forms.CharField(max_length=1024, required=False)
    processed = forms.BooleanField(required=False)

    small = forms.CharField(max_length=6400000, required=False)
    medium = forms.CharField(max_length=6400000, required=False)
    large = forms.CharField(max_length=6400000, required=False)
    huge = forms.CharField(max_length=6400000, required=False)

    rszformat = forms.CharField(max_length=4, required=False)
    source = forms.CharField(max_length=256, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        uid = cleaned_data.pop("uid")

        try:
            rszformat = cleaned_data.pop("rszformat").lower()
            if rszformat not in ("jpg", "png"):
                raise forms.ValidationError("format is other than png or jpg")
        except:
            rszformat = None
            for item in ("small", "medium", "large", "huge"):
                if cleaned_data.get(item):
                    msg = "no rszformat provided (resize format: png/jpg)"
                    raise forms.ValidationError(msg)

        for item in ("small", "medium", "large", "huge"):
            if cleaned_data.get(item):
                mime = rszformat
                if mime == "jpg":
                    mime = "jpeg"
                name = "mlfw%d_%s.%s" % (uid, item, rszformat)
                cleaned_data[item] = SimpleUploadedFile(
                    name,
                    base64.b64decode(cleaned_data[item]),
                    content_type="image/%s" % mime
                )
        try:
            name = self.cleaned_data.pop("name")
            image = self.cleaned_data.pop("image")
        except:
            name = None
            image = None
            try:
                self.cleaned_data.pop("image")
            except:
                pass

        for item in ("png", "gif", "webp", "jpg"):
            if cleaned_data.get(item):
                mime = item
                if mime == "jpg":
                    mime = "jpeg"
                cleaned_data[item] = SimpleUploadedFile(
                    "mlfw" + str(uid) + "." + item,
                    base64.b64decode(cleaned_data[item]),
                    content_type="image/%s" % mime
                )

        if name and image:
            mime = name.rpartition(".")[2]
            if mime == "jpg":
                mime = "jpeg"
            cleaned_data["image"] = SimpleUploadedFile(
                name,
                base64.b64decode(image),
                content_type="image/%s" % mime
            )
        return cleaned_data


class CreateFace(forms.Form):
    name = forms.CharField(max_length=240)
    image_data = forms.CharField(max_length=10000000)
    tags = forms.CharField(max_length=256, required=False)
    source = forms.CharField(max_length=256, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            #image should be like:
            #data:image/png;base64,3ranfadf...
            image = cleaned_data.pop("image_data")
            part = image.partition(":")[2].partition(";")
            #mime = part[0]
            part = image.partition(",")
            image = base64.b64decode(part[2])
        except:
            raise forms.ValidationError("No image supplied")
        name = cleaned_data.pop("name")
        ext = name.rpartition(".")[2].lower()
        if ext == "jpg":
            ext = "jpeg"
        cleaned_data["image"] = SimpleUploadedFile(
            name,
            image,
            content_type="image/%s" % ext
        )
        cleaned_data["accepted"] = False
        return cleaned_data


class NewCreateFace(forms.Form):
    image = forms.CharField(max_length=10000000)
    tags = forms.CharField(max_length=256, required=False)
    source = forms.CharField(max_length=256, required=False)

    def clean(self):
        try:
            #image should be like:
            #data:image/png;base64,3ranfadf...
            imagedataraw = self.cleaned_data.pop("image")
            try:
                imagedata = json.loads(imagedataraw)
            except:
                imagedata = json.loads(imagedataraw.replace("'", '"'))
            print imagedata.keys()
            mime = imagedata["mime"]
            filename = imagedata["filename"]
            image = base64.b64decode(imagedata["base64"])
        except:
            raise forms.ValidationError("No valid image data supplied")
        self.cleaned_data["image"] = SimpleUploadedFile(
            filename,
            image,
            content_type=mime
        )
        self.cleaned_data["accepted"] = False
        print self.cleaned_data
        return self.cleaned_data


class Settings(forms.Form):
    """
    Users can set some settings with this form.
    """
    PONIES = (
        # ("derpy_hooves", "Derpy Hooves"),
        # ("fluttershy", "Fluttershy"),
        ("rarity", "Rarity"),
        # ("twilight_sparkle", "Twilight Sparkle"),
        # ("minimalis", "Minimalis"),
    )

    # no_webp = forms.BooleanField(label="Disable webp", required=False)
    best_pony = forms.ChoiceField(label="Best pony:", choices=PONIES)


class SubmitForm(forms.Form):
    """
    Submit images.
    """
    image = forms.ImageField(
        label="Image*",
        widget=forms.FileInput(attrs={"multiple": "multiple"})
    )
    tags = forms.CharField(label="Tags", required=False)
    source = forms.CharField(label="Source", required=False)


class Vote(forms.Form):
    vote = forms.CharField(required=True)

    def clean(self):
        if self.cleaned_data["vode"] not in ("up", "down"):
            raise forms.ValidationError("Invalid vote")
        return self.cleaned_data
