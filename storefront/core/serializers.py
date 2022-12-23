from djoser.serializers import \
    UserCreateSerializer as UserCreateSerializerFromDjoser, \
    UserSerializer as UserSerializerFromDjoser

from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializerFromDjoser):

    class Meta(UserCreateSerializerFromDjoser.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(UserSerializerFromDjoser):
    class Meta(UserSerializerFromDjoser.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
