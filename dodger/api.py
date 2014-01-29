from django.contrib.auth.models import User

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource


class UserResource(ModelResource):
    """a resource for Users"""

    class Meta:
        # how to call resource
        resource_name = 'users'
        queryset = User.objects.all()
        # limit fields
        excludes = ('password', 'is_superuser')
        # available methods - limit to get, all other work should be done in admin
        list_allowed_methods = ('get', )
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'date_joined': ALL,
            'email': ALL,
            'first_name': ALL,
            'id': ALL,
            'is_active': ALL,
            'is_staff': ALL,
            'last_login': ALL,
            'last_name': ALL,
            'username': ALL
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True
