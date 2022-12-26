from django.urls import path
from rest_framework.routers import DefaultRouter
from .apis import SpendingApi, spendingReportApi

router = DefaultRouter()
router.register(prefix="spending", viewset=SpendingApi, basename="spending")

urlpatterns = [
    path("spending-report/<int:weeks>/", spendingReportApi, name="spending_report")

]
urlpatterns += router.urls
