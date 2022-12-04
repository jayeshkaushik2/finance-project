from . import apis
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("token/", apis.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("create-user/", apis.CreateUserApi, name="create-user"),
    # path(
    #     "validate-siginup-otp/", apis.validate_Signup_otp, name="validate-siginup-otp"
    # ),
    # path("user-profile/", apis.user_profileApi, name="user-profile"),
    # path("forgot-password/", apis.forgot_passwordApi, name="forgot-password"),
    # path(
    #     "validate-forgotpass-otp/",
    #     apis.validate_forgot_password_otpApi,
    #     name="validate-forgotpass-otp",
    # ),
    # path("change-password/", apis.change_passwordApi, name="change-password"),
    # path("user-orders/<int:user_id>/", apis.user_ordersApi, name="user-orders"),
]

urlpatterns += router.urls
