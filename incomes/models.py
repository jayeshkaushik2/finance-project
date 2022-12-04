from django.db import models

# Create your models here.
class Income(models.Model):
    source = models.CharField(max_length=256, null=True, blank=True)
    salary = models.PositiveBigIntegerField(null=True, blank=True, default=0)
