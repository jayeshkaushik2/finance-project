from django.urls import path
from rest_framework.routers import DefaultRouter
from .apis import IncomeApi, incomeReportApi

router = DefaultRouter()
router.register(prefix="income", viewset=IncomeApi, basename="income")

urlpatterns = [
    path("income-report/<int:weeks>/", incomeReportApi, name="income_report")
]
urlpatterns += router.urls
