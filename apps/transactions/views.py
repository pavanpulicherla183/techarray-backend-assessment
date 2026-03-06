from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionDetailView(generics.RetrieveAPIView):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    queryset = Transaction.objects.select_related("batch")