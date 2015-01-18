from __future__ import unicode_literals
import logging
import operator
from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters, viewsets

from dpdapi.filters import AliasRegexFilterBackend
from dpdapi.models import Alias, Domain, User
from dpdapi.serializers import AliasSerializer, AliasDeleteSerializer, DomainSerializer, UserSerializer


logger = logging.getLogger(__name__)


class AliasViewSet(viewsets.ModelViewSet):
    """ Aliases """
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, AliasRegexFilterBackend)
    filter_fields = ('domain', 'domain__name',)

    @list_route(methods=['post'])
    def create_bulk(self, request):
        serializer = AliasSerializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @list_route(methods=['delete'])
    def delete_bulk(self, request):
        serializer = AliasDeleteSerializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)

        # Ref: http://michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/
        q_list = map(lambda x: Q(**x), serializer.initial_data)
        aliases = Alias.objects.filter(reduce(operator.or_, q_list))

        initial_set = set(map(lambda x: (x['source'], x['destination'], x['domain']), serializer.initial_data))
        deleted_set = set(aliases.values_list('source', 'destination', 'domain'))
        diff = initial_set.difference(deleted_set)
        logger.debug('Deleted: {}'.format(','.join(map(lambda x: '{0[0]}={0[1]}'.format(x), deleted_set))))
        aliases.delete()

        if diff:
            diff_formatted = map(lambda x: '{0[0]}={0[1]}'.format(x), diff)
            res = "Aliases '{}' could not be found and were not deleted.".format(", ".join(diff_formatted))
            logger.info(res)
            return Response({"result": res}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)


class DomainViewSet(viewsets.ModelViewSet):
    """ Domains """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    """ Users """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
