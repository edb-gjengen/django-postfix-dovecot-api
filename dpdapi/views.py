from __future__ import unicode_literals
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters, viewsets

from .models import Alias, Domain, User
from .serializers import AliasSerializer, AliasIdSerializer, DomainSerializer, UserSerializer


class AliasViewSet(viewsets.ModelViewSet):
    """ Aliases """
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('domain', 'domain__name')

    @list_route(methods=['post'])
    def create_bulk(self, request):
        serializer = AliasSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['delete'])
    def delete_bulk(self, request):
        # TODO how to lookup instances and delete them by id?
        serializer = AliasIdSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ids = map(lambda x: x['id'], serializer.initial_data)  # FIXME this is not how to do it
        aliases = Alias.objects.filter(id__in=ids)
        diff = set(ids).difference(set(aliases.values_list('id', flat=True)))
        aliases.delete()

        if diff:
            result = "ID's '{}' could not be found and were not deleted.".format(", ".join(map(str, diff)))
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
