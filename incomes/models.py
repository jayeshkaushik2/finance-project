from django.db import models
from common.models import TimeStampMixin

# Create your models here.


class Income(TimeStampMixin, models.Model):
    user = models.ForeignKey("accounts.user", on_delete=models.CASCADE, related_name="income")
    source = models.CharField(max_length=256, null=True, blank=True)
    salary = models.PositiveBigIntegerField(null=True, blank=True, default=0)
