from django.db import models
from common.models import TimeStampMixin

# Create your models here.
class Spending(TimeStampMixin, models.Model):
    user = models.ForeignKey(
        "accounts.user", on_delete=models.CASCADE, related_name="spending"
    )
    spent_on = models.CharField(max_length=256, null=True, blank=True)
    spent_money = models.PositiveBigIntegerField(null=True, blank=True, default=0)
