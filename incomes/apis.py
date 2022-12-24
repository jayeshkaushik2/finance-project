from rest_framework import decorators, permissions
from rest_framework import viewsets, exceptions

# local imports
from .models import Income
from .serializers import IncomeSz


class IncomeApi(viewsets.ModelViewSet):
    serializer_class = IncomeSz
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
