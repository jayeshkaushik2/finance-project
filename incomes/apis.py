from rest_framework import decorators, permissions
from rest_framework import viewsets, exceptions

# local imports
from .models import Income
from .serializers import IncomeSz


class IncomeApi(viewsets.ModelViewSet):
    serializer_class = IncomeSz

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Income.objects.all(user=self.request.user)
        return None

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise exceptions.ValidationError("Your are not logged in.")
        return serializer.save(user=self.request.user)
