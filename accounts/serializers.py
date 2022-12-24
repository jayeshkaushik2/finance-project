from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginUserValidationSz(serializers.Serializer):
    email = serializers.CharField(required=False)
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
            "tokens",
        )

    def get_token(self, obj):
        t = RefreshToken.for_user(user=obj)
        tokens = dict(access=str(t.access_token), refresh=str(t))
        return tokens
