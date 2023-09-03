from rest_framework import serializers
from rest_framework.authtoken.models import Token

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "last_login", "token"]

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key


def get_serialized_user(user, many=False):
    return UserSerializer(user).data
