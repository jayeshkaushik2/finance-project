from rest_framework import decorators, permissions
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response

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


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def spendingReportApi(request, weeks):
    user = request.user
    current_date = timezone.now().date()
    previous_date = timezone.now().date() - timedelta(weeks=int(weeks))
    incomes = Spending.objects.filter(user=user, created_at__date__gte=previous_date)
    sz = SpendingSz(instance=incomes, many=True)
    return Response(sz.data)
