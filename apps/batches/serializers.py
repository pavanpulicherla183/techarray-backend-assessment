from rest_framework import serializers
from .models import BatchJob
from apps.transactions.serializers import TransactionSerializer


class BatchJobSerializer(serializers.ModelSerializer):

    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = BatchJob
        fields = [
            "id",
            "client",
            "status",
            "transactions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]


class BatchCreateSerializer(serializers.Serializer):

    transactions = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )