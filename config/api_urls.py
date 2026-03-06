from django.urls import path

from apps.batches.views import (
    BatchCreateView,
    BatchListView,
    BatchDetailView
)

from apps.transactions.views import TransactionDetailView


urlpatterns = [

    path("batches/", BatchCreateView.as_view()),
    path("batches/list/", BatchListView.as_view()),
    path("batches/<uuid:pk>/", BatchDetailView.as_view()),

    path("transactions/<uuid:pk>/", TransactionDetailView.as_view()),
]