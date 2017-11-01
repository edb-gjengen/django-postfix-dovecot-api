import django_filters
from rest_framework.filters import BaseFilterBackend

from dpdapi.models import Alias


class AliasRegexFilter(django_filters.FilterSet):
    class Meta:
        model = Alias
        fields = {
            'source': ['iregex', 'regex'],
            'destination': ['iregex', 'regex']
        }


class AliasRegexFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return AliasRegexFilter(request.query_params, queryset=queryset).qs
