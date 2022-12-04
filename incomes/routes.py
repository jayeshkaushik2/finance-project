from django.urls import path
from rest_framework.routers import DefaultRouter
from .apis import IncomeApi

router = DefaultRouter()
router.register(prefix="income", viewset=IncomeApi, basename="income")

urlpatterns = []
urlpatterns += router.urls
