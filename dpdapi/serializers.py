from rest_framework import serializers

from .models import Alias, Domain, User


class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias


class AliasIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = ['id']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User