from rest_framework import serializers
from users.models import User


class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.SlugField()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'bio', 'email', 'role')