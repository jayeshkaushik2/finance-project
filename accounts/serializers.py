from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginUserValidationSz(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = PhoneNumberField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        if "email" not in attrs and "mobile" not in attrs:
            raise exceptions.ValidationError(
                {"errors": ["Email or Mobile is required."]}
            )
        return attrs


class UserLoginSz(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField("get_token")

    class Meta:
        model = User
        fields = (
            "id",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
            "is_verified",
            "tokens",
        )

    def get_token(self, obj):
        t = RefreshToken.for_user(user=obj)
        tokens = dict(access=str(t.access_token), refresh=str(t))
        return tokens


class RegisterUserValidationSz(serializers.Serializer):
    # Mobile is Optional
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile = PhoneNumberField(required=False)
    password = serializers.CharField(required=True)


class UserDetailSz(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "mobile",
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
            "profile_image",
            "banner_image",
            "is_verified",
        )
        read_only_fields = ("email",)
