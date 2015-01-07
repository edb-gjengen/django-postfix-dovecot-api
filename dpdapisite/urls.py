from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
    url(r'^api/', include('dpdapi.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='api-root')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
