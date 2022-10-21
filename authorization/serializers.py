from django.core.exceptions import ValidationError
from rest_framework import serializers
from authorization import models  # noqa:


class UserSerializer(serializers.ModelSerializer):
    identifier = serializers.ReadOnlyField()
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = models.User
        fields = ["identifier", "username", "email", "name", "surname", "password"]

    def validate(self, data):  # noqa:W0221
        return data



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):  # noqa:W0221
        if models.User.objects.filter(username=data["username"]).exists():
            raise ValidationError(f"User with username {data['username']} already exists!")
        return data