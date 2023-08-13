from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from common.ImageBase64 import Base64ImageField

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
    profile_image = serializers.SerializerMethodField()

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
            "tokens",
        )

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if not obj.profile_image:
            return ""
        photo_url = obj.profile_image.url
        return request.build_absolute_uri(photo_url)

    def get_token(self, obj):
        t = RefreshToken.for_user(user=obj)
        tokens = dict(access=str(t.access_token), refresh=str(t))
        return tokens


class RegisterUserValidationSz(serializers.Serializer):
    # Mobile is Optional
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile = PhoneNumberField(required=False)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise exceptions.ValidationError({"errors": ["Passwords does not match."]})
        return super().validate(attrs)


class UserDetailSz(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None, use_url=True, required=False)
    banner_image = Base64ImageField(max_length=None, use_url=True, required=False)

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


class VerifyOtpValidationSz(serializers.Serializer):
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        otp = attrs.get("otp")
        if len(otp) != 5:
            raise exceptions.ValidationError({"errors": ["Invalid OTP"]})
        return super().validate(attrs)
