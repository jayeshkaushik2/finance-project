from rest_framework import decorators, permissions, viewsets
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

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


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def incomeReportApi(request, weeks):
    user = request.user
    current_date = timezone.now().date()
    previous_date = timezone.now().date() - timedelta(weeks=int(weeks))
    incomes = Income.objects.filter(user=user, created_at__date__gte=previous_date)
    sz = IncomeSz(instance=incomes, many=True)
    return Response(sz.data)
