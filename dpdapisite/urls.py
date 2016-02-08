from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework import urls as rest_framework_urls

from dpdapi import urls as dpdapi_urls


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='api-root')),
    url(r'^api/', include(dpdapi_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include(rest_framework_urls, namespace='rest_framework'))
]
