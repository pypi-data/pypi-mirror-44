"""djangoldp project URL Configuration"""
from importlib import import_module

from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.models import Group, User
from djangoldp.views import LDPViewSet
from djangoldp.permissions import AnonymousReadOnly

from .models import ChatProfile, Account
from .views import userinfocustom, RedirectView

djangoldp_modules = list(filter(lambda app: app.startswith('djangoldp_'), settings.INSTALLED_APPS))
user_fields = ['@id', 'first_name', 'groups', 'last_name', 'username', 'email', 'account', 'chatProfile', 'name']
user_nested_fields = ['account', 'groups', 'chatProfile']
for dldp_module in djangoldp_modules:
    try:
        user_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
        user_nested_fields += import_module(dldp_module + '.settings').USER_NESTED_FIELDS
    except:
        pass

urlpatterns = [
    url(r'^groups/', LDPViewSet.urls(model=Group, fields=['@id', 'name', 'user_set'], permission_classes=[AnonymousReadOnly])),
    url(r'^users/', LDPViewSet.urls(model=settings.AUTH_USER_MODEL, fields=user_fields, permission_classes=[AnonymousReadOnly],
                                    nested_fields=user_nested_fields )),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/redirect/$', RedirectView.as_view(), name="redirect_login"),
    url(r'^accounts/', LDPViewSet.urls(model=Account, permission_classes=[AnonymousReadOnly])),
    url(r'^chat-profile/', LDPViewSet.urls(model=ChatProfile, permission_classes=[AnonymousReadOnly])),
    url(r'^openid/userinfo', userinfocustom),
    url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
]

s_fields = []
s_fields.extend(user_fields)
s_fields.extend(user_nested_fields)
User._meta.serializer_fields = s_fields
Group._meta.serializer_fields = ['name']