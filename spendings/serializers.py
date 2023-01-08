from rest_framework import serializers
from .models import Spending


class SpendingSz(serializers.ModelSerializer):
    month = serializers.SerializerMethodField("get_month")

    class Meta:
        model = Spending
        fields = (
            "id",
            "spent_on",
            "spent_money",
            "month",
            "created_at",
            "updated_at",
        )

    def get_month(self, obj):
        if obj.created_at is not None:
            return obj.created_at.strftime("%B")
        return ""
