from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'api/', include('app.api')),

    # app views
    url(r'^', include('app.urls', namespace='app')),
)
