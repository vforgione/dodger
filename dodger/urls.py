from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns(
    '',

    # home
    url(r'^$', TemplateView.as_view(template_name='dodger/home.html')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'api/', include('app.api')),

    # app views
    url(r'^', include('app.urls', namespace='app')),
)
