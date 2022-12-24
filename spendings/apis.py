from rest_framework import decorators, permissions
from rest_framework import viewsets, exceptions

# local imports
from .models import Spending
from .serializers import SpendingSz


class SpendingApi(viewsets.ModelViewSet):
    serializer_class = SpendingSz
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
