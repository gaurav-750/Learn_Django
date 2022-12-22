from djoser.serializers import UserCreateSerializer \
    as UserCreateSerializerFromDjoser
from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializerFromDjoser):

    class Meta(UserCreateSerializerFromDjoser.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
