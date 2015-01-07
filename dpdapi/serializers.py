from rest_framework import serializers
from passlib.hash import sha512_crypt
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
        extra_kwargs = {'password': {'write_only': True}}

    def _hash_password(self, raw_password):
        return sha512_crypt.encrypt(raw_password)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            domain=validated_data['domain'],
            password=self._hash_password(validated_data['password'])
        )
        user.save()
        return user
