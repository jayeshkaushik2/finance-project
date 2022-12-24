from django.urls import path
from rest_framework.routers import DefaultRouter
from .apis import SpendingApi

router = DefaultRouter()
router.register(prefix="spending", viewset=SpendingApi, basename="spending")

urlpatterns = []
urlpatterns += router.urls
