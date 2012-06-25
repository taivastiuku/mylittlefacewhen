from django.conf import settings

from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from piston.resource import Resource

from viewer.resources import *
from viewer import authentication
from viewer import feeds

from viewer.api import v2

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#these are for api mapping and api access control for the old piston-api (v1)
faces_handler = Resource(FacesHandler, authentication = authentication.AnonMethodAllowed().set_allowed(["GET", "POST", "PUT"]))
search_handler = Resource(SearchHandler)
tags_handler = Resource(TagsHandler)
feedback_handler = Resource(FeedbackHandler, authentication = authentication.AnonMethodAllowed().set_allowed(["POST"]))
login_handler = Resource(LoginHandler)
detect_handler = Resource(DetectHandler)
report_handler = Resource(ReportHandler, authentication =authentication.AnonMethodAllowed().set_allowed(["POST",]))


urlpatterns = patterns('',
    #PAGE
    (r'^$', "viewer.views.main"),
    (r'^search/$', "viewer.views.search"),
    (r'^s/$', "viewer.views.search"),
#    (r'^(f|face)/(?P<face_id>\d+)/qr/$', "viewer.views.qr"),
    (r'^f/(?P<face_id>\d+)/?', "viewer.views.single"),
    (r'^face/(?P<face_id>\d+)/?', "viewer.views.single"),
    (r'^randoms/?$', "viewer.views.randoms"),
    # I wanted to do (f|face|random) but it had some problem.
    (r'^random/?$', "viewer.views.rand"),
    (r'^face/?$', "viewer.views.rand"),
    (r'^f/?$', "viewer.views.rand"),
#    (r'^salute/(?P<salute_id>\d+)/$', "viewer.views.salute"),
#    (r'^salute/$', "viewer.views.salute"),
    (r'^develop/?$', "viewer.views.develop"),
    (r'^develop/api', "viewer.views.api"),
    (r'^feedback/?$', "viewer.views.feedback"),
    (r'^submit/?$', "viewer.views.submit"),
    (r'^tags/?$', "viewer.views.tags"),
    (r'^unreviewed/?$', "viewer.views.main", {"listing":"unreviewed"}),
#    (r'^toplist/$', "viewer.views.main", {"listing":"toplist"}),
#    (r'^toplist/(?P<page>\d+)/$', "viewer.views.main", {"listing":"toplist"}),
    (r'^changelog/?$', "viewer.views.changelog"),

#    (r'^errors/500/$', "viewer.views.error"),
#    (r'^errors/404/$', "viewer.views.notfound"),
    
    #admin
    (r'^taglog/$', "viewer.views.taglog"),
    (r'^taglog/(?P<page>\d+)/$', "viewer.views.taglog"),
    (r'^sourcelog/$', "viewer.views.sourcelog"),
    (r'^sourcelog/(?P<page>\d+)/$', "viewer.views.sourcelog"),
    (r'^acceptimages/$', "viewer.views.acceptImages"),

    #RSS
    (r'^feed/$', feeds.LatestAcceptedImages()),

    #Django registration
    (r'^accounts/', include('registration.urls')),
    
    #API v1 (deprecated)
    url(r'^api/faces/?$', faces_handler),
    url(r'^api/faces/(?P<uid>[^/]+)/?$', faces_handler),
    url(r'^api/search/?', search_handler),
    url(r'^api/tags/?', tags_handler),
    url(r'^api/feedback/?$', feedback_handler),
    url(r'^api/feedback/(?P<uid>[^/]+)/?$', feedback_handler),
    url(r'^api/login/?$', login_handler),
    url(r'^api/detect/$', detect_handler),
    url(r'^api/report/$', report_handler),

    #API v2
    url(r'^api/', include(v2.API.urls)),

    #RESIZOR
#    url(r'^api/resizor/$', resizor),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += staticfiles_urlpatterns()

handler404 = "viewer.views.notfound"
handler500 = "viewer.views.error"
