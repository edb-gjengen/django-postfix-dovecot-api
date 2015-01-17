from __future__ import unicode_literals
import logging
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters, viewsets

from dpdapi.filters import AliasRegexFilterBackend
from dpdapi.models import Alias, Domain, User
from dpdapi.serializers import AliasSerializer, AliasIdSerializer, DomainSerializer, UserSerializer


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['delete'])
    def delete_bulk(self, request):
        # FIXME, accept [{source: kak@stry.no, destination: lol@lol.com}] instead of IDs
        serializer = AliasIdSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ids = map(lambda x: x['id'], serializer.initial_data)  # FIXME this might not be too great
        aliases = Alias.objects.filter(id__in=ids)
        diff = set(ids).difference(set(aliases.values_list('id', flat=True)))
        logger.debug('Deleted: {}'.format(','.join(map(unicode, aliases))))
        aliases.delete()

        if diff:
            res = "ID's '{}' could not be found and were not deleted.".format(", ".join(map(unicode, diff)))
            logger.info(res)
            result = res
            return Response({"result": result}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)


class DomainViewSet(viewsets.ModelViewSet):
    """ Domains """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """ Users """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
