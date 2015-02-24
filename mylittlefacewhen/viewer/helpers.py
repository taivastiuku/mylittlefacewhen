UPDATED = 17

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def standard_r2r(function):
    from django.http import HttpResponse
    from django.shortcuts import render_to_response
    from django.template import RequestContext

    def inner(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        try:
            template, to_template = response
        except ValueError:
            pass
        else:
            response = template

        if isinstance(response, HttpResponse):
            return response

        to_template.update({"updated": UPDATED})
#            "url": request.resolver_match.url_name})

        return render_to_response(
            template,
            to_template,
            context_instance=RequestContext(request))

    return inner


def get_meta(request, title=None, description=None):
    from django.conf import settings
    meta = {
        "path": request.path,
        "static_prefix": settings.STATIC_URL,
        "title": "Pony Reaction Pictures",
        "description": "Express yourself with ponies",
        "default_image": settings.STATIC_URL + "cheerilee-square-300.png"}

    if title is not None:
        meta["title"] = title
    if description is not None:
        meta["description"] = description

    return meta
