import django_filters

from dpdapi.models import Alias

from django_filters import filters

filters.LOOKUP_TYPES = ['iregex', 'exact', 'iexact']


class AliasFilter(django_filters.FilterSet):
    # TODO: These do not work
    # Ref: https://docs.djangoproject.com/en/1.7/ref/models/querysets/#iregex
    source_regex = django_filters.CharFilter(name='source', lookup_expr=['iregex'])
    destination_regex = django_filters.CharFilter(name='destination', lookup_expr=['iregex'])

    class Meta:
        model = Alias
        fields = ['domain', 'domain__name', 'source_regex', 'destination_regex']
