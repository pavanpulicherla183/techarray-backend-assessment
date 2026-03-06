import time
import random

from celery import shared_task

from .models import Transaction, TransactionStatus
from apps.batches.models import BatchJob, BatchStatus


def mock_validation_service(payload):
    """
    Simulates external API call
    """

    time.sleep(random.randint(3, 5))

    if random.random() < 0.2:
        raise Exception("External service failed")

    return {
        "valid": True,
        "checked_at": time.time()
    }


@shared_task(bind=True, max_retries=3)
def process_transaction(self, transaction_id):

    try:

        transaction = Transaction.objects.get(id=transaction_id)

        transaction.status = TransactionStatus.PROCESSING
        transaction.save(update_fields=["status"])

        result = mock_validation_service(transaction.payload)

        transaction.validation_result = result
        transaction.status = TransactionStatus.COMPLETED
        transaction.save()

    except Exception as exc:

        transaction.status = TransactionStatus.FAILED
        transaction.attempts += 1
        transaction.save()

        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

    update_batch_status(transaction.batch_id)


def update_batch_status(batch_id):

    batch = BatchJob.objects.get(id=batch_id)

    transactions = batch.transactions.all()

    if transactions.filter(status__in=["pending", "processing"]).exists():
        batch.status = BatchStatus.PROCESSING
    elif transactions.filter(status="failed").exists():
        batch.status = BatchStatus.FAILED
    else:
        batch.status = BatchStatus.COMPLETED

    batch.save(update_fields=["status"])