from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.http import HttpResponse


admin.autodiscover()


def logout_page(request):
    logout(request)
    return redirect('/')


urlpatterns = patterns(
    '',

    # robots one liner
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),

    # login/out
    # url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^accounts/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/logout/$', logout_page),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'^api/', include('app.api')),

    # app views
    url(r'^', include('app.urls', namespace='app')),
)
