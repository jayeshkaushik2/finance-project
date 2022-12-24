from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import exceptions
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from rest_framework import decorators, exceptions
from django.contrib.auth import get_user_model
import django_filters
from .serializers import LoginUserValidationSz, UserLoginSz
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

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

        return Response(UserLoginSz(instance=user).data)
    else:
        raise exceptions.ValidationError(
            {"errors": ["Please Provide a valid information."]}
        )
