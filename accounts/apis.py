from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db.models import Q
from rest_framework import decorators, exceptions, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    LoginUserValidationSz,
    RegisterUserValidationSz,
    UserDetailSz,
    UserLoginSz,
)

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@decorators.api_view(["POST"])
def loginUserApi(request):
    sz = LoginUserValidationSz(data=request.data)
    if sz.is_valid(raise_exception=True):
        password = sz.validated_data.get("password")
        email = sz.validated_data.get("email")
        if email is not None:
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response(
                    {"errors": ["User not found."]}, status=HTTP_404_NOT_FOUND
                )
            is_valid = user.check_password(password)
            if not is_valid:
                return Response(
                    {"errors": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST
                )

        else:
            mobile = sz.validated_data.get("mobile")
            user = User.objects.filter(mobile=mobile).first()
            if user is None:
                return Response(
                    {"errors": ["User not found."]}, status=HTTP_404_NOT_FOUND
                )
            is_valid = user.check_password(password)
            if not is_valid:
                return Response(
                    {"errors": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST
                )

        return Response(UserLoginSz(instance=user, context={"request": request}).data)


@decorators.api_view(["POST"])
def registerUserApi(request):
    sz = RegisterUserValidationSz(data=request.data)
    if sz.is_valid(raise_exception=True):
        email = sz.validated_data.get("email")
        mobile = sz.validated_data.get("mobile")
        password = sz.validated_data.pop("password")
        user = User.objects.filter(Q(email=email) | Q(mobile=mobile))
        if user.count() > 0:
            return Response(
                {"errors": ["User with email or mobile already exists."]},
                status=HTTP_400_BAD_REQUEST,
            )
        user = User.objects.create(**request.data)
        user.set_password(password)
        user.save()
        # TODO have to send OTP to the user email or mobile to verify the User
        return Response(UserLoginSz(instance=user, context={"request": request}).data)
    else:
        raise exceptions.ValidationError(
            {"errors": ["Please Provide a valid information."]}
        )


@decorators.api_view(["GET", "POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
def UserDetailApi(request):
    user = request.user
    if request.method == "GET":
        sz = UserDetailSz(instance=user, context=dict(request=request))
        return Response(sz.data)
    else:
        # for password update
        if "password" in request.data:
            password = request.data.pop("password")
            user.set_password(password)
            user.save()
        # for mobile update
        if "mobile" in request.data:
            mobile = request.data.get("mobile")
            found_user = User.objects.filter(mobile=mobile).first()
            if found_user is not None and found_user != user:
                return Response(
                    {"errors": ["Mobile number already exists."]},
                    status=HTTP_400_BAD_REQUEST,
                )
        # for other detail update
        sz = UserDetailSz(
            instance=user,
            data=request.data,
            partial=True,
            context=dict(request=request),
        )
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)
        raise exceptions.ValidationError(
            {"errors": ["Please Provide a valid information."]}
        )
