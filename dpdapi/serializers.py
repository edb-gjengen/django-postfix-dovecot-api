from rest_framework import serializers
from passlib.hash import sha512_crypt
from .models import Alias, Domain, User


class AliasSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # Workaround to accept duplicates
        # FIXME, will fail with existing alias with validated_data['active']=False
        alias, created = Alias.objects.get_or_create(**validated_data)
        return alias

    class Meta:
        model = Alias
        validators = []  # Disable unique togheter check
        fields = '__all__'


class AliasDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        validators = []  # No Unique togheter check on deletion


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
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
