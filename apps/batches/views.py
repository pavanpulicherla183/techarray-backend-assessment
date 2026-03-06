from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import BatchJob
from .serializers import BatchJobSerializer, BatchCreateSerializer

from apps.transactions.models import Transaction
from apps.transactions.tasks import process_transaction


class BatchCreateView(generics.CreateAPIView):

    serializer_class = BatchCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transactions_data = serializer.validated_data["transactions"]

        # create batch
        batch = BatchJob.objects.create(client=request.user)

        # create transaction objects
        transaction_objects = [
            Transaction(batch=batch, payload=tx)
            for tx in transactions_data
        ]

        # bulk insert transactions
        Transaction.objects.bulk_create(transaction_objects)

        # fetch created transactions
        created_transactions = Transaction.objects.filter(batch=batch)

        # queue celery tasks
        for tx in created_transactions:
            process_transaction.delay(str(tx.id))

        return Response(
            {"batch_id": batch.id},
            status=status.HTTP_202_ACCEPTED
        )


class BatchListView(generics.ListAPIView):

    serializer_class = BatchJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            BatchJob.objects
            .filter(client=self.request.user)
            .prefetch_related("transactions")
        )


class BatchDetailView(generics.RetrieveAPIView):

    serializer_class = BatchJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            BatchJob.objects
            .filter(client=self.request.user)
            .prefetch_related("transactions")
        )