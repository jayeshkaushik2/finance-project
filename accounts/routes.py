from . import apis
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("token/", apis.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", apis.loginUserApi, name="login"),
    path("signup/", apis.registerUserApi, name="register_user"),
    path("resend-otp/", apis.resend_otp, name="resend_otp"),
    path("verify-otp/", apis.verify_otp, name="verify_otp"),
    path("user-details/", apis.UserDetailApi, name="user_details"),
]

urlpatterns += router.urls
