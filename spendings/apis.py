from rest_framework import decorators, permissions
from rest_framework import viewsets, exceptions

# local imports
from .models import Spending
from .serializers import SpendingSz


class SpendingApi(viewsets.ModelViewSet):
    serializer_class = SpendingSz

    def get_queryset(self):
        if self.request.user is not None and self.request.user.is_authenticated:
            return Spending.objects.filter(user=self.request.user)
        return None

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise exceptions.ValidationError("Your are not logged in.")
        return serializer.save(user=self.request.user)
