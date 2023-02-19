from rest_framework import decorators, permissions, viewsets, exceptions
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

# local imports
from .models import Income
from .serializers import IncomeSz
from django.db.models import Sum, F
from common.customPagination import CustomPagination


class IncomeApi(viewsets.ModelViewSet):
    serializer_class = IncomeSz
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def incomeReportApi(request, weeks):
    user = request.user
    previous_date = timezone.now().date() - timedelta(weeks=int(weeks))
    incomes = Income.objects.filter(user=user, created_at__date__gte=previous_date)
    sz = IncomeSz(instance=incomes, many=True)
    return Response(sz.data)


from spendings.models import Spending


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def SummaryReportApi(request):
    user = request.user
    current_month = timezone.now().date().strftime("%m")

    current_month_incomes = Income.objects.filter(
        user=user, created_at__date__month=current_month
    ).aggregate(Sum("salary"))

    current_month_spendings = Spending.objects.filter(
        user=user, created_at__date__month=current_month
    ).aggregate(Sum("spent_money"))

    if current_month_incomes is None or current_month_spendings is None:
        raise exceptions.NotFound({"errors": ["Data not found."]})
    data = dict(
        total_income=current_month_incomes["salary__sum"],
        total_spending=current_month_spendings["spent_money__sum"],
        total_saving=current_month_incomes["salary__sum"]
        - current_month_spendings["spent_money__sum"],
    )
    return Response(data)
