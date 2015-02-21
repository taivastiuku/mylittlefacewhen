from django.conf import settings

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from viewer import feeds, views

from viewer.api import v2
from viewer.api import v3

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    #PAGE
    url(r'^$', views.main, name="index"),
    url(r'^new/?$', views.main, {"listing": "new"}, name="new"),
    url(r'^hot/?$', views.main, {"listing": "hot"}, name="hot"),
    url(r'^popular/?$', views.main, {"listing": "popular"}, name="popular"),
    url(r'^unreviewed/?$', views.main, {"listing": "unreviewed"}, name="unreviewed"),
    url(r'^search/$', views.search, name="search"),
    url(r'^s/$', views.search, name="s"),
    # (r'^(f|face)/(?P<face_id>\d+)/qr/$', "viewer.views.qr"),
    url(r'^f/(?P<face_id>\d+)/?', views.single, name="f"),
    url(r'^face/(?P<face_id>\d+)/?', views.single, name="face"),
    url(r'^randoms/?$', views.randoms, name="randoms"),
    # I wanted to do (f|face|random) but it had some problem.
    url(r'^random/?$', views.rand, name="random"),
    url(r'^face/?$', views.rand),
    url(r'^f/?$', views.rand),
    # (r'^salute/(?P<salute_id>\d+)/$', "viewer.views.salute"),
    # (r'^salute/$', "viewer.views.salute"),
    url(r'^develop/?$', views.develop, name="develop"),
    url(r'^develop/api', views.api, name="api"),
    url(r'^feedback/?$', views.feedback, name="feedback"),
    url(r'^submit/?$', views.submit, name="submit"),
    url(r'^tags/?$', views.tags, name="tags"),
    # (r'^toplist/$', views.main", {"listing":"toplist"}),
    # (r'^toplist/(?P<page>\d+)/$', "viewer.views.main",{"listing":"toplist"}),
    url(r'^changelog/?$', views.changelog, name="changelog"),

    # (r'^errors/500/$', "viewer.views.error"),
    # (r'^errors/404/$', "viewer.views.notfound"),

    #RSS
    url(r'^feed/$', feeds.LatestAcceptedImages(), name="feed"),

    #Django registration
    #(r'^accounts/', include('registration.urls')),

    # Tastypie APIs
    url(r'^api/', include(v2.API.urls)),
    url(r'^api/', include(v3.API.urls)),

    #RESIZOR
    # url(r'^api/resizor/$', resizor),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "viewer.views.notfound"
handler500 = "viewer.views.error"
