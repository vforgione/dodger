from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView


admin.autodiscover()


def logout_page(request):
    logout(request)
    return redirect('/')


urlpatterns = patterns(
    '',

    # home
    url(r'^$', TemplateView.as_view(template_name='dodger/home.html')),

    # login/out
    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', logout_page),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'^api/', include('app.api')),

    # app views
    url(r'^', include('app.urls', namespace='app')),
)
