from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dat.views',
    # home
    url(r'^home/$', 'home', name='home'),

    # purchase orders
    url(r'^po(?:/(?P<pk>\d+|\d+\-[a-zA-Z]+))?/$', 'po_view', name='po-view'),
    url(r'^po/create/$', 'po_create', name='po-create'),
)
