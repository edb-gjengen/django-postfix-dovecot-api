import django_filters

from dpdapi.models import Alias


class AliasRegexFilter(django_filters.FilterSet):
    # Ref: https://docs.djangoproject.com/en/1.7/ref/models/querysets/#iregex
    source_regexp = django_filters.CharFilter(name="source", lookup_type='iregex')

    class Meta:
        model = Alias
        fields = ['source_regexp']