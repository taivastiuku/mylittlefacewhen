from datetime import datetime, timedelta

from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.utils.html import strip_spaces_between_tags

PONIES = ("rarity",)


class ContentTypeMiddleware(object):
    def process_request(self, request):
        if request.method in ['PUT'] and request.META['CONTENT_TYPE'].count(";") > 0:
            request.META['CONTENT_TYPE'] = [c.strip() for c in request.META['CONTENT_TYPE'].split(";")][0]
        return None

# Opera supported .webp from ver 11.10


class RedirectIE9(object):
    """
    Internet Explorer doesnt support pushstate history. This breaks links
    opened by IE, pasted by other browsers and we need to redirect IE to
    hashed url.
    """
    def process_request(self, request):
        if request.META.get("HTTP_USER_AGENT", "").find("MSIE 9.0") != -1 and request.path != "/" and not request.path.startswith("/api/"):
            to = ""
            if request.is_secure():
                to += "https://"
            else:
                to += "http://"
            to += request.get_host() + "/#" + request.path[1:]

            return HttpResponseRedirect(to)
        else:
            return None


class RedirectDomain(object):
    """
    I want everyone to use the main domain so 302 for "www." subdomain and for
    mlfw.info shortener.
    """
    def process_request(self, request):
        host = request.META.get("HTTP_HOST")
        if not host:
            return None
        if host not in ("mylittlefacewhen.com", "tiuku.me:8888"):
            url = "http://mylittlefacewhen.com" + request.path
            return HttpResponsePermanentRedirect(url)


class SpacelessHTML(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = strip_spaces_between_tags(response.content)
        return response


class Style(object):
    def process_request(self, request):
        pony = request.GET.get("best_pony")
        if pony:
            try:
                request.COOKIES.pop("best_pony")
            except:
                pass
        else:
            pony = request.COOKIES.get("best_pony")

        if pony not in PONIES:
            #request.best_pony = random.choice(PONIES)
            request.best_pony = "rarity"
        else:
            request.best_pony = pony
        return None

    def process_response(self, request, response):
        pony = request.COOKIES.get("best_pony", "")
        if pony not in PONIES:
            expires = datetime.utcnow() + timedelta(days=365)
            try:
                best_pony = request.best_pony
            except:
                return response
            response.set_cookie("best_pony", value=best_pony, expires=expires, httponly=True)
        return response


class NoCache(object):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class AllowPieforkMiddleware(object):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            return HttpResponse()

    def process_response(self, request, response):
        if  request.META.get('HTTP_ORIGIN'):
            response['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT, PATCH'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
