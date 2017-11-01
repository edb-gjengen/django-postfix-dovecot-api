import django_filters

from dpdapi.models import Alias

from django_filters import filters

filters.LOOKUP_TYPES = ['iregex', 'exact', 'iexact']


class AliasFilter(django_filters.FilterSet):
    # TODO: These do not work
    # Ref: https://docs.djangoproject.com/en/1.7/ref/models/querysets/#iregex
    source_regex = django_filters.CharFilter(name='source')
    destination_regex = django_filters.CharFilter(name='destination')

    class Meta:
        model = Alias
        fields = {
            'domain': ['exact'],
            'domain__name': ['iexact'],
            'source_regex': ['iregex', 'regex'],
            'destination_regex': ['iregex', 'regex']
        }
