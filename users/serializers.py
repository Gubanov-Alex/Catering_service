from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()


class UserRegistratrionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
        ]

    def validate(self, attrs: dict) -> dict:
        """Change the password for its hash to make token validation available"""

        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "role"]


class UserActivationSerializer(serializers.Serializer):
    key = serializers.UUIDField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            "password": attrs.get("password"),
        }

        from django.contrib.auth import authenticate
        user = authenticate(**credentials)


        if user is None or not user.is_active:
            raise AuthenticationFailed("User account is not active. Please activate it.")

        self.user = user
        data = super().validate(attrs)

        return data

