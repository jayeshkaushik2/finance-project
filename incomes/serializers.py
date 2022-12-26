from rest_framework import serializers
from .models import Income


class IncomeSz(serializers.ModelSerializer):
    month = serializers.SerializerMethodField("get_month")

    class Meta:
        model = Income
        fields = (
            "id",
            "user",
            "source",
            "salary",
            "month",
            "created_at",
            "updated_at",
        )

    def get_month(self, obj):
        if obj.created_at is not None:
            return obj.created_at.strftime("%B")
        return ""
