import django_filters

from dpdapi.models import Alias
from rest_framework.filters import BaseFilterBackend


class AliasRegexFilter(django_filters.FilterSet):
    # Ref: https://docs.djangoproject.com/en/1.7/ref/models/querysets/#iregex
    source_regex = django_filters.CharFilter(name="source", lookup_type='iregex')
    destination_regex = django_filters.CharFilter(name="destination", lookup_type='iregex')

    class Meta:
        model = Alias


class AliasRegexFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return AliasRegexFilter(request.query_params, queryset=queryset).qs
