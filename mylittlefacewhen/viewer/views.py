from datetime import datetime

#from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from viewer.models import *
from viewer import forms

IMAGEURL = "http://denver.mylittlefacewhen.com"

STATIC_PREFIX = "/static/"

DEFAULT_META = {
        "static_prefix":STATIC_PREFIX,
        "title": "Pony Reaction Pictures",
        "description": "Lots of well-tagged pony reaction images, add yours!",
        "default_image": STATIC_PREFIX + "cheerilee-square-300.png",
    }



def main(request, listing="normal"):
    """
    Handles index and toplist listings.
    """
    # No appcache for firefox due to suspicious popups
    not_firefox = request.META.get("HTTP_USER_AGENT", "").lower().find("firefox") == -1

    if listing == "normal":
        path = "/"
    else:
        path = "/" + listing + "/"

    meta = DEFAULT_META.copy()
    meta["path"] = request.path

    to_template = {
            "listing" : listing,
            "path" : path,
            "not_firefox" : not_firefox,
            "content": "main.mustache",
            "content_data": {"static_prefix":STATIC_PREFIX},
            "metadata": DEFAULT_META,
            }

    ret = render_to_response("backbone.html", to_template, context_instance = RequestContext(request))
    return ret

def randoms(request):
    """
    list of random images
    """

    meta = DEFAULT_META.copy()
    meta["title"] = "Random ponies!"
    meta["description"] = "Endless list of reacting ponies that just goes on and on and on... "
    meta["path"] = request.path

    to_template = {
            "content": "randoms.mustache",
            "content_data": {"static_prefix":STATIC_PREFIX},
            "metadata": meta,
            }
    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))

def search(request):
    """
    List of all the reactions with given tag.
    """
    query = request.GET.get("tag", request.GET.get("tags", "")).strip(",")
    tags = [tag.strip() for tag in query.split(",")]
    faces = Face.search(tags)

    if len(faces) == 1:
	return redirect("/f/%d" % faces[0].id)
    elif len(faces) == 0:
        query = "Search by typing some tags into the searchbox __^"
    else:
        query = query + ", "

    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Search for "
    for tag in tags:
        meta["title"] += tag + ", "
    meta["description"] = "You can search ponies with one or more tags"

    to_template = {
            "content": "search.mustache",
            "content_data": {
                "static_prefix":STATIC_PREFIX,
                "query" : query
                },
            "metadata": meta,
            }

    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))

def single(request, face_id):
    """
    Single face with given id.
    """
    face = get_object_or_404(Face, id=face_id)
    if face.duplicate_of:
        return redirect("/f/%d/" % face.duplicate_of.id, permanent=True)

    image = face.get_image("large")
    face.setThumb(webp=False, gif=True)
    if face.accepted:
        imageurl = IMAGEURL
    else:
        imageurl = "http://" + request.get_host()

    f = model_to_dict(face, fields=["source","accepted","id", "width", "height"])
    if f.get("source"):
        f["source"] = [f["source"]]

    f["tags"] = [{"name":tag.name} for tag in face.tags]

    f["image"] = face.image.url

    f["resizes"] = []
    for itm in ("huge","large","medium","small"):
        if getattr(face, itm):
            f["resizes"].append({"image":getattr(face, itm).url, "size": itm})

    artist, title, description = face.getMeta()

    to_content = {
            "artist": artist,
            "face": f,
            "thumb":getattr(face.thumb, "url", None), #Avoid error when no thumb has been generated
            "image":image,
            "static_prefix": STATIC_PREFIX,
            "image_service": imageurl,
            "alt": description,
            }

    to_template = {
            "content": "single.mustache",
            "content_data": to_content,
            "metadata": {
                "title": title,
                "description": description,
                "static_prefix": STATIC_PREFIX,
                "default_image": imageurl + f["image"],
                "path": request.path,
                "alt_image": True,
                "canonical": "http://mylittlefacewhen.com/f/" + str(f["id"]) + "/",
                },
            }

    return render_to_response("backbone.html", to_template, context_instance=RequestContext(request))

def develop(request):
    """
    Info page about the site.
    """

    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Information"
    meta["description"] = "Details about mylittlefacewhen.com development and future"

    to_template = {
            "content": "develop.mustache",
            "content_data": {},
            "metadata": meta,
            }
    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))


def api(request):
    """
    API documentation
    """
    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "API documentation"
    meta["description"] = "Most of the site can be created using only this API"
    to_template = {
            "content": "apidoc-v2.mustache",
            "content_data": {},
            "metadata": meta,
            }
    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))

def rand(request):
    """
    Redirect to random face.
    """
    face = Face.random()
    return redirect("/f/%d/" % face.id)

#def salute(request, salute_id=None):
#    """
#    Lists all saluteimages
#    """
#    if salute_id:
#        salute = get_object_or_404(Salute, id=salute_id)
#    else:
#	salute = _getSalute(request)
#
#    to_template = {
#            "salute" : salute,
#            "salutes" : Salute.objects.all(),
#            }
#
#    return render_to_response("viewer/salute.html", to_template, context_instance = RequestContext(request))


@login_required
def changes(request, page=1):
    page = int(page)
    start = 30*(page-1)
    end = 30*+page
    changelog_id = request.POST.get("id")
    undo = None
    if changelog_id:
        ret = ChangeLog.objects.filter(id=changelog_id)
        if ret:
            undo = ret[0].undo()
    faces = []
    logs = ChangeLog.objects.all().order_by("-datetime")[start:end]
    for log in logs:
        face = log.face
        face.setThumbWithRequest(request)
        faces.append(face)

    z = zip(logs, faces)

    to_template = {
            "zip" : z,
            "undo" : undo,
        }

    return render_to_response("changes.html", to_template, context_instance=RequestContext(request))


@csrf_exempt
def feedback(request):
    if request.method == "POST":
	form = forms.FeedbackForm(request.POST, request.FILES)
	if form.is_valid():
	    filu = form.cleaned_data.get("file")
	    feedback = Feedback(contact=form.cleaned_data.get("contact"), text=form.cleaned_data.get("feedback"), datetime=datetime.utcnow(), image = filu)
	    feedback.save()
	    form = forms.FeedbackForm()
	    message = "Thanks for your feedback!"
	else:
	    message = "There were errors"
    else:
        message = "Submit feedback:"
	form = forms.FeedbackForm()

    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Feedback"
    meta["description"] = "Any feedback is welcome, bug reports are highly appreciated"
    to_template = {
            "content": "feedback.mustache",
            "content_data": {"message" : message},
            "metadata": meta,
        }
    return render_to_response("backbone.html", to_template, context_instance=RequestContext(request))


def submit(request):

    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Upload ponies!"
    meta["description"] = "Sharing is caring!"
    to_template = {
            "content": "submit.mustache",
            "content_data": {"static_prefix":STATIC_PREFIX},
            "metadata": meta,
            }
    return render_to_response("backbone.html", to_template, context_instance=RequestContext(request))

def tags(request):
    """
    View all tags
    """
    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Tags"
    meta["description"] = "Some popular tags with random images and all the tags as links"
    to_template = {
            "content": "tags.mustache",
            "content_data": {"models": [{"name":tag.name} for tag in Face.tags.all()]},
            "metadata": meta,
            }

    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))

def changelog(request):
    meta = DEFAULT_META.copy()
    meta["path"] = request.path
    meta["title"] = "Changelog"
    meta["description"] = "We've come a long way. Another day another release."
    to_template = {
            "content": "changelog.mustache",
            "content_data": {},
            "metadata": meta,
            }
    return render_to_response("backbone.html", to_template, context_instance = RequestContext(request))

@login_required
def acceptImages(request):
    faces = Face.objects.filter(accepted=False).order_by("-id")
    for face in faces:
        face.setThumbWithRequest(request)

    to_template = {
            "faces" : faces,
        }
    return render_to_response("acceptimages.html", to_template, context_instance = RequestContext(request))

@login_required
def viewFlags(request):
    flags = Flag.objects.all()

    for flag in flags:
        flag.face.setThumbWithRequest(request)

    to_template = {
            "flags": flags,
            }
    return render_to_response("flags.html", to_template, context_instance = RequestContext(request))

@login_required
def md5Duplicates(request):
    duplicateSets = []
    duplicateIds = []
    for face in Face.objects.all():
        if not face.md5:
            continue
        faces = Face.objects.filter(md5=face.md5)
        if len(faces) > 1:
            cont = False
            for f in faces:
                if f.id in duplicateIds:
                    cont = True
                    break
                duplicateIds.append(f.id)
            if cont:
                continue

            out = []
            for f in faces:
                f.setThumb(webp=False, gif=True)
                out.append(f)

            duplicateSets.append(out)

    to_template = {"dupeslist": duplicateSets}

    return render_to_response("duplicates.html", to_template, context_instance = RequestContext(request))




def notfound(request):
    to_template = {}
    return render_to_response("404.html", to_template, context_instance = RequestContext(request))

def error(request):
    raise Exception("Test error")
    to_template = {
            "form" : forms.FeedbackForm()
        }
    return render_to_response("500.html", to_template, context_instance = RequestContext(request))
