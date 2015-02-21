from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from . import forms, models
from .helpers import standard_r2r, get_meta

IMAGEURL = "http://pinkie.mylittlefacewhen.com"

@standard_r2r
def main(request, listing="normal"):
    """
    Handles index and toplist listings.
    """
    # No appcache for firefox due to suspicious popups
    user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
    not_firefox = user_agent.find("firefox") == -1

    path = "/" if listing == "normal" else "/" + listing + "/"

    to_template = {
        "listing": listing,
        "path": path,
        "not_firefox": not_firefox or True,
        "content": "main.mustache",
        "content_data": {"static_prefix": settings.STATIC_URL},
        "metadata": get_meta(request)}

    return "backbone.html", to_template


@standard_r2r
def randoms(request):
    """
    list of random images
    """
    to_template = {
        "content": "randoms.mustache",
        "content_data": {"static_prefix": settings.STATIC_URL},
        "metadata": get_meta(
            request,
            "Random ponies!",
            "Endless list of reacting ponies that just goes on and on and on...")}

    return "backbone.html", to_template


@standard_r2r
def search(request):
    """
    List of all the reactions with given tag.
    """
    query = request.GET.get("tag", request.GET.get("tags", "")).strip(",")
    tags = [tag.strip() for tag in query.split(",")]
    faces = models.Face.tagged.with_all(tags)

    if len(faces) == 1:
        return redirect("/f/%d" % faces[0].id)
    elif len(faces) == 0:
        query = "Search by typing some tags into the searchbox __^"
    else:
        query = query + ", "

    to_template = {
        "content": "search.mustache",
        "content_data": {
            "static_prefix": settings.STATIC_URL,
            "query": query},
        "metadata": get_meta(
            request,
            "Search for " + ", ".join(tags),
            "You can search ponies with one or more tags.")}

    return "backbone.html", to_template


@standard_r2r
def single(request, face_id):
    """
    Single face with given id.
    """
    face = get_object_or_404(models.Face, id=face_id)
    if face.duplicate_of:
        return redirect("/f/%d/" % face.duplicate_of.id, permanent=True)
    if face.removed is True:
        raise Http404

    image = face.get_image("large")
    face.setThumb(webp=False, gif=True)
    if face.accepted:
        imageurl = IMAGEURL
    else:
        imageurl = "http://" + request.get_host()

    attrs = ("source", "accepted", "id", "width", "height", "comments",
             "artist", "title", "description")

    f = {attr: getattr(face, attr) for attr in attrs}

    f.update({
        "tags": [{"name":tag.name} for tag in face.tags],
        "image": face.image.url,
        "resizes": [{"size":size, "image": image} for size, image in face.resizes.items()]})

    artist, title, description = face.getMeta()

    to_content = {
        "face": f,
        # Avoid error when no thumb has been generated:
        "thumb": getattr(face.thumb, "url", None),
        "image": image,
        "static_prefix": settings.STATIC_URL,
        "image_service": imageurl,
        "alt": f["description"]}

    to_template = {
        "content": "single.mustache",
        "content_data": to_content,
        "metadata": {
            "title": title,
            "description": description,
            "static_prefix": settings.STATIC_URL,
            "default_image": imageurl + f["image"],
            "path": request.path,
            "alt_image": True,
            "canonical": "http://mylittlefacewhen.com/f/%s/" % str(f["id"])}}

    return "backbone.html", to_template


@standard_r2r
def develop(request):
    """
    Info page about the site.
    """
    to_template = {
        "content": "develop.mustache",
        "content_data": {},
        "metadata": get_meta(
            request,
            "Information",
            "Details about mylittlefacewhen.com development and future.")}

    return "backbone.html", to_template


@standard_r2r
def api(request):
    """
    API documentation
    """
    to_template = {
        "content": "apidoc-v3.mustache",
        "content_data": {},
        "metadata": get_meta(
            request,
            "API documentation",
            "Most of the site can be created using only this API.")}

    return "backbone.html", to_template


def rand(request):
    """
    Redirect to random face.
    """
    return redirect("/f/%d/" % models.Face.random().id)


@csrf_exempt
@standard_r2r
def feedback(request):
    if request.method == "POST":
        form = forms.FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            filu = form.cleaned_data.get("file")
            feedback = models.Feedback(
                contact=form.cleaned_data.get("contact"),
                text=form.cleaned_data.get("feedback"),
                datetime=datetime.utcnow(),
                image=filu)
            feedback.save()
            form = forms.FeedbackForm()
            message = "Thanks for your feedback!"
        else:
            message = "There were errors"
    else:
        message = "Submit feedback:"
        form = forms.FeedbackForm()

    to_template = {
        "content": "feedback.mustache",
        "content_data": {"message": message},
        "metadata": get_meta(
            request,
            "Feedback",
            "Any feedback is welcome, bug reports are highly appreciated")}

    return "backbone.html", to_template


@standard_r2r
def submit(request):
    to_template = {
        "content": "submit.mustache",
        "content_data": {"static_prefix": settings.STATIC_URL},
        "metadata": get_meta(
            request,
            "Upload ponies!",
            "Sharing is caring!")}

    return "backbone.html", to_template


@standard_r2r
def tags(request):
    """
    View all tags
    """
    to_template = {
        "content": "tags.mustache",
        "content_data": {
            "models": [{"name": tag} for tag in models.Face.tags.values_list("name", flat=True)]},
        "metadata": get_meta(
            request,
            "Tags",
            "Some popular tags with random images and all the tags as links")}

    return "backbone.html", to_template


@standard_r2r
def changelog(request):
    to_template = {
        "content": "changelog.mustache",
        "content_data": {},
        "metadata": get_meta(
            request,
            "Changelog",
            "We've come a long way. Another day another release.")}

    return "backbone.html", to_template


@standard_r2r
def notfound(request):
    return "404.html", {}


@standard_r2r
def error(request):
    raise Exception("Test error")
    return "500.html", {"form": forms.FeedbackForm()}
