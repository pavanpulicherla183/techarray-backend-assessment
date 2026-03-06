from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "batch",
            "payload",
            "status",
            "validation_result",
            "attempts",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "validation_result",
            "attempts",
            "created_at",
            "updated_at",
        ]